from aiogram import F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Url, Group
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.states.trip import TripSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.core.data.db.dao import DaoHolder


async def trip_getter(
        dialog_manager: DialogManager, dao: DaoHolder, add_message_viewer: AdditionalMessageViewer,
        **__
):
    trip_id = dialog_manager.dialog_data["trip_id"]
    trip = await dao.trip.get(trip_id)
    if trip.medias:
        await add_message_viewer.send(trip.medias)

    return {"trip": trip}


trip_window = Window(
    Format("<b>{trip.name}</b>\n"),
    Format(
        text="{trip.description}",
        when=F["trip"].description,
    ),

    Group(
        Url(
            text=Const("Сайт 🌐"),
            url=Format("{trip.site_url}"),
            id="site_url",
            when=F["trip"].site_url
        ),
        width=2,
    ),
    buttons.BACK,
    getter=trip_getter,
    state=TripSG.trip
)
