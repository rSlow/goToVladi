from aiogram import types, F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.hotel import HotelSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import HotelDao


@inject
async def district_getter(dao: FromDishka[HotelDao], user: dto.User, **__):
    districts = await dao.get_all_districts(user.region.id)
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
        width=4
    ),
    buttons.CANCEL,
    state=HotelSG.district,
    getter=district_getter
)


@inject
async def hotels_getter(dao: FromDishka[HotelDao], dialog_manager: DialogManager, **__):
    district_id = dialog_manager.dialog_data["district_id"]
    hotels = await dao.get_filtered_list(district_id=district_id)
    return {"hotels": hotels}


async def on_hotel_click(_, __, manager: DialogManager, hotel_id: str):
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
        height=4,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=HotelSG.hotel_list,
    getter=hotels_getter
)
