from aiogram import F
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import BarCardSG, BarListSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import BarDao


@inject
async def bars_getter(dao: FromDishka[BarDao], user: dto.User, **__):
    bars = await dao.get_all_from_region(region_id=user.region.id)
    region = user.region
    return {
        "bars": bars,
        "region": region
    }


async def on_bar_click(_, __, manager: DialogManager, bar_id: str):
    await manager.start(BarCardSG.state, data={"bar_id": int(bar_id)})


category_bar_dialog = Dialog(
    Window(
        Format(
            "Бары в <b>{region.name}</b>:",
            when=F["bars"]
        ),
        Format(
            "К сожалению, в <b>{region.name}</b> мы еще не добавили бары. Скоро добавим!",
            when=~F["bars"]
        ),
        ScrollingGroup(
            Select(
                text=Format("{item.name}"),
                id="bars",
                items="bars",
                item_id_getter=dto.id_getter,
                on_click=on_bar_click
            ),
            id="bars_scroll",
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        buttons.CANCEL,
        state=BarListSG.state,
        getter=bars_getter
    )
)
