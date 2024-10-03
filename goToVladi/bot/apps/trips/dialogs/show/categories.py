from aiogram import types, F
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.window import Window

from goToVladi.bot.apps.trips.states import TripSG
from goToVladi.bot.utils import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder


async def trips_getter(dao: DaoHolder, user: dto.User, **__):
    region = user.region
    trips = await dao.trip.get_filtered_list(region.id_)
    return {
        "trips": trips,
        "region": region,
    }


async def on_trip_click(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, trip_id: str
):
    manager.dialog_data["trip_id"] = int(trip_id)
    await manager.next()


list_trips_window = Window(
    Format(
        "Доступные экскурсии в <b>{region.name}</b>:",
        when=F["trips"]
    ),
    Format(
        "К сожалению, в <b>{region.name}</b> мы еще не добавили экскурсий, "
        "но мы уже усердно отбираем для Вас лучшие маршруты!",
        when=~F["trips"]
    ),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            id="trips",
            items="trips",
            item_id_getter=dto.id_getter,
            on_click=on_trip_click
        ),
        id="trips_scroll",
        width=1,
        height=5,
        hide_on_single_page=True,
    ),
    buttons.CANCEL,
    getter=trips_getter,
    state=TripSG.trip_list
)
