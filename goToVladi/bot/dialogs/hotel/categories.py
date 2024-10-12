from aiogram import types, F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.states.hotel import HotelSG
from goToVladi.bot.views import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder


async def district_getter(dao: DaoHolder, user: dto.User, **__):
    districts = await dao.hotel.get_all_districts(user.region.id_)
    return {"districts": districts}


async def set_district(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, district_id: str
):
    manager.dialog_data["district_id"] = int(district_id)
    await manager.next()


district_window = Window(
    Const("Выберите район отеля:"),
    Group(
        Select(
            Format("{item.name}"),
            id="districts",
            item_id_getter=dto.id_getter,
            items="districts",
            on_click=set_district
        ),
        width=3
    ),
    buttons.CANCEL,
    state=HotelSG.district,
    getter=district_getter
)


async def hotels_getter(dao: DaoHolder, dialog_manager: DialogManager, **__):
    district_id = dialog_manager.dialog_data["district_id"]
    hotels = await dao.hotel.get_filtered_list(district_id=district_id)
    return {"hotels": hotels}


async def on_hotel_click(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, hotel_id: str
):
    manager.dialog_data["hotel_id"] = int(hotel_id)
    await manager.next()


list_hotels_window = Window(
    Const(
        "Выберите отель:",
        when=F["hotels"]
    ),
    Const(
        "К сожалению, в этот район мы пока еще не добавили отели, "
        "но сделаем это в самое ближайшее время!",
        when=~F["hotels"]
    ),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            item_id_getter=dto.id_getter,
            id="hotels",
            items="hotels",
            on_click=on_hotel_click,
        ),
        id="hotels_scroll",
        width=1,
        height=3,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=HotelSG.hotels,
    getter=hotels_getter
)
