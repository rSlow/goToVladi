from aiogram import F
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.massage import MassageCardSG, MassageListSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao.massage import MassageDao


@inject
async def massages_getter(massage_dao: FromDishka[MassageDao], user: dto.User, **__):
    massages = await massage_dao.get_all_from_region(region_id=user.region.id)
    region = user.region
    return {
        "massages": massages,
        "region": region
    }


async def on_massage_click(_, __, manager: DialogManager, massage_id: str):
    await manager.start(MassageCardSG.state, data={"massage_id": int(massage_id)})


category_massage_dialog = Dialog(
    Window(
        Format(
            "Массажные салоны в <b>{region.name}</b>:",
            when=F["massages"]
        ),
        Format(
            "К сожалению, в <b>{region.name}</b> мы еще не добавили массажные салоны. "
            "Скоро добавим!",
            when=~F["massages"]
        ),
        ScrollingGroup(
            Select(
                text=Format("{item.name}"),
                id="massages",
                items="massages",
                item_id_getter=dto.id_getter,
                on_click=on_massage_click
            ),
            id="massages_scroll",
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        buttons.CANCEL,
        state=MassageListSG.state,
        getter=massages_getter
    )
)
