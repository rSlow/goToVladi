from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Group, Select
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.sea_recreation import SeaRecreationListSG, SeaRecreationCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import SeaRecreationDao


@inject
async def categories_getter(sea_recreation_dao: FromDishka[SeaRecreationDao], user: dto.User, **__):
    categories = await sea_recreation_dao.get_all_categories(user.region.id)
    return {
        "categories": categories,
        "region": user.region
    }


async def set_category(_, __, manager: DialogManager, category_id: str):
    manager.dialog_data["category_id"] = int(category_id)
    await manager.next()


categories_window = Window(
    Format(
        "Выберите нужную категорию:",
        when=F["categories"]
    ),
    Format(
        "К сожалению, в <b>{region.name}</b> мы еще не добавили точек отдыха на море, "
        "но мы уже усердно работаем над этим!",
        when=~F["categories"]
    ),

    Group(
        Select(
            Format("{item.name}"),
            id="categories",
            item_id_getter=dto.id_getter,
            items="categories",
            on_click=set_category
        ),
        width=4
    ),
    buttons.CANCEL,
    state=SeaRecreationListSG.category,
    getter=categories_getter
)


@inject
async def sea_recreations_getter(
        dao: FromDishka[SeaRecreationDao], dialog_manager: DialogManager, **__
):
    category_id = dialog_manager.dialog_data["category_id"]
    sea_recreations = await dao.get_filtered_list(category_id=category_id)
    category = await dao.get_category(category_id)
    return {
        "sea_recreations": sea_recreations,
        "category": category
    }


async def on_sea_recreation_click(_, __, manager: DialogManager, sea_recreation_id: str):
    await manager.start(
        SeaRecreationCardSG.state, data={"sea_recreation_id": int(sea_recreation_id)}
    )


sea_recreations_list_window = Window(
    Format(
        "Доступно в категории {category.name}",
        when=F["sea_recreations"]
    ),
    Format(
        "К сожалению, в этот район мы пока еще не добавили точки отдыха в категорию "
        "{category.name}, но сделаем это в самое ближайшее время!",
        when=~F["sea_recreations"]
    ),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            item_id_getter=dto.id_getter,
            id="sea_recreations",
            items="sea_recreations",
            on_click=on_sea_recreation_click,
        ),
        id="sea_recreations_scroll",
        width=1,
        height=4,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=SeaRecreationListSG.sea_recreation_list,
    getter=sea_recreations_getter
)

category_sea_recreation_dialog = Dialog(
    categories_window,
    sea_recreations_list_window
)
