from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import SwitchTo, Select
from aiogram_dialog.widgets.text import Format, Case, Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.filters.region import has_region
from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.states.region import RegionSG
from goToVladi.bot.views import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import RegionDao, UserDao


async def main_region_getter(user: dto.User, **__):
    return {"user": user}


start_window = Window(
    Format(
        text="Установлен регион <u><b>{user.region.name}</b></u>",
        when=has_region
    ),
    Format(
        text="Регион поиска не установлен. Нажмите кнопку 'Установить регион'.",
        when=~has_region
    ),
    SwitchTo(
        id="set_region",
        text=Case(
            texts={
                True: Const("Сменить регион"),
                ...: Const("Установить регион"),  # default value
            },
            selector=has_region
        ),
        state=RegionSG.set
    ),
    buttons.CANCEL,
    getter=main_region_getter,
    state=RegionSG.start
)


@inject
async def regions_getter(dao: FromDishka[RegionDao], **__):
    regions = await dao.get_all()
    return {"regions": regions}


@inject
async def on_region_click(
        callback: types.CallbackQuery, _, manager: DialogManager, region_id: str,
        user_dao:FromDishka[UserDao]
):
    middleware_data: MiddlewareData = manager.middleware_data
    user = middleware_data["user"]

    await user_dao.set_region(tg_id=user.tg_id, region_id=int(region_id))

    updated_user = await user_dao.get_by_tg_id(user.tg_id)
    await callback.message.answer(f"❗️ Установлен регион: {updated_user.region.name}")
    middleware_data["user"] = updated_user

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


set_region_window = Window(
    Const("Доступные регионы:"),
    Select(
        text=Format("{item.name}"),
        id="regions",
        items="regions",
        item_id_getter=dto.id_getter,
        on_click=on_region_click
    ),
    buttons.BACK,
    getter=regions_getter,
    state=RegionSG.set
)

region_dialog = Dialog(
    start_window,
    set_region_window,
)
