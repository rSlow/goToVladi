from aiogram import F, types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import SwitchTo, Select
from aiogram_dialog.widgets.text import Format, Case, Const

from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.states.region import RegionSG
from goToVladi.bot.views import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder

has_region = F["user"].region.is_not(None)


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


async def regions_getter(dao: DaoHolder, **__):
    regions = await dao.region.get_all()
    return {"regions": regions}


async def on_region_click(
        callback: types.CallbackQuery, _: Select,
        manager: DialogManager, region_id: str
):
    middleware_data: MiddlewareData = manager.middleware_data
    dao = middleware_data["dao"]
    user = middleware_data["user"]

    await dao.user.set_region(tg_id=user.tg_id, region_id=int(region_id))

    saver_user = await dao.user.get_by_tg_id(user.tg_id)
    await callback.message.answer(
        f"❗️ Установлен регион: {saver_user.region.name}"
    )
    middleware_data["user"] = saver_user

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
