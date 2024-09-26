from operator import itemgetter

from aiogram import types, F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select, ScrollingGroup, Url
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.hotels.states import HotelSG
from goToVladi.bot.utils import buttons
from goToVladi.bot.views.media_group import send_additional_media_group
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder


async def district_getter(dao: DaoHolder, **__):
    districts = await dao.hotel.get_all_districts()
    return {
        "districts": [*enumerate(districts, 1)]
    }


async def set_district(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, district: str
):
    manager.dialog_data["district"] = district
    await manager.next()


district_window = Window(
    Const("Выберите район отеля:"),
    Group(
        Select(
            Format("{item[1]}"),
            id="districts",
            item_id_getter=itemgetter(0),
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
    district = dialog_manager.dialog_data["district"]
    hotels = await dao.hotel.get_filtered_list(district=district)
    return {"hotels": hotels}


async def on_hotel_click(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, hotel_id: str
):
    hotel_id = manager.dialog_data["hotel_id"] = int(hotel_id)
    await manager.next()


list_hotels_window = Window(
    Const("Выберите отель:"),
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
    state=HotelSG.hotels,
    getter=hotels_getter
)


async def hotel_getter(dao: DaoHolder, dialog_manager: DialogManager,
                       message: types.Message):
    hotel_id = dialog_manager.dialog_data["hotel_id"]
    hotel = await dao.hotel.get(hotel_id)

    if hotel.medias:
        await send_additional_media_group(
            medias=hotel.medias, message=message, manager=dialog_manager
        )

    return {"hotel": hotel}


DESCRIPTION_SCROLL = "description_scroll"

hotel_window = Window(
    Format("<b>{hotel.name}</b>\n"),
    Format("Цена номера от {hotel.min_price} ₽\n"),
    Format(
        text="{hotel.description}",
        when=F["hotel"].description,
    ),

    Group(
        Url(
            text=Const("Сайт 🌐"),
            url=Format("{hotel.site_url}"),
            id="site_url",
            when=F["hotel"].site_url
        ),
    ),
    state=HotelSG.hotel
)

show_dialog = Dialog(
    district_window,
    list_hotels_window,
    hotel_window
)
