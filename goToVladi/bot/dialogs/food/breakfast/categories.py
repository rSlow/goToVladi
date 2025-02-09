from aiogram import F
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import BreakfastCardSG, BreakfastListSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import BreakfastDao


@inject
async def breakfasts_getter(dao: FromDishka[BreakfastDao], user: dto.User, **__):
    breakfasts = await dao.get_all_from_region(region_id=user.region.id)
    return {
        "breakfasts": breakfasts,
        "region": user.region
    }


async def on_breakfast_click(_, __, manager: DialogManager, breakfast_id: str):
    await manager.start(BreakfastCardSG.state, data={"breakfast_id": int(breakfast_id)})


category_breakfast_dialog = Dialog(
    Window(
        Format(
            "Завтраки в <b>{region.name}</b>:",
            when=F["breakfasts"]
        ),
        Format(
            "К сожалению, в <b>{region.name}</b> мы еще не добавили завтраки. Скоро добавим!",
            when=~F["breakfasts"]
        ),
        ScrollingGroup(
            Select(
                text=Format("{item.name}"),
                id="breakfasts",
                items="breakfasts",
                item_id_getter=dto.id_getter,
                on_click=on_breakfast_click
            ),
            id="breakfasts_scroll",
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        buttons.CANCEL,
        state=BreakfastListSG.state,
        getter=breakfasts_getter
    )
)
