from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import DeliveryListSG, DeliveryCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DeliveryDao


@inject
async def get_cuisines(dao: FromDishka[DeliveryDao], user: dto.User, **__):
    cuisines = await dao.get_all_cuisines(region_id=user.region.id)
    region = user.region
    return {
        "cuisines": cuisines,
        "region": region
    }


async def set_cuisine(_, __, manager: DialogManager, cuisine_id: str):
    manager.dialog_data["cuisine_id"] = int(cuisine_id)
    await manager.next()


cuisines_window = Window(
    Const(
        "Выберите тип кухни:",
        when=F["cuisines"]
    ),
    Format(
        "К сожалению, в <b>{region.name}</b> мы еще не добавили доставки еды. Скоро добавим!",
        when=~F["cuisines"]
    ),
    Group(
        Select(
            Format("{item.name}"),
            id="cuisines",
            item_id_getter=dto.id_getter,
            items="cuisines",
            on_click=set_cuisine
        ),
        width=3
    ),
    buttons.CANCEL,
    state=DeliveryListSG.cuisines,
    getter=get_cuisines
)


@inject
async def get_deliveries(
        dao: FromDishka[DeliveryDao], dialog_manager: DialogManager, user: dto.User, **__
):
    cuisine_id = dialog_manager.dialog_data["cuisine_id"]
    deliveries = await dao.get_list_by_cuisine(cuisine_id=cuisine_id, region_id=user.region.id)
    return {"deliveries": deliveries}


async def on_delivery_click(_, __, manager: DialogManager, delivery_id: str):
    await manager.start(DeliveryCardSG.state, data={"delivery_id": int(delivery_id)})


deliveries_window = Window(
    Const(
        "Выберите доставку:",
        when=F["deliveries"]
    ),
    Const(
        f"В данной категории пока нет доставок, но мы обязательно скоро добавим!",
        when=~F["deliveries"]
    ),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            item_id_getter=dto.id_getter,
            id="delivery",
            items="deliveries",
            on_click=on_delivery_click,
        ),
        id="deliveries_scroll",
        width=1,
        height=3,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=DeliveryListSG.delivery_list,
    getter=get_deliveries
)

delivery_list_dialog = Dialog(
    cuisines_window,
    deliveries_window
)
