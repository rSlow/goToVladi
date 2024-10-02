from aiogram import F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Url
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.hotels.states import HotelSG
from goToVladi.bot.utils import buttons
from goToVladi.bot.views.media_group import send_additional_media_group
from goToVladi.core.data.db.dao import DaoHolder


async def hotel_getter(dao: DaoHolder, dialog_manager: DialogManager, **__):
    hotel_id = dialog_manager.dialog_data["hotel_id"]
    hotel = await dao.hotel.get(hotel_id)

    if hotel.medias:
        await send_additional_media_group(
            medias=hotel.medias, manager=dialog_manager
        )

    return {"hotel": hotel}


DESCRIPTION_SCROLL = "description_scroll"

hotel_window = Window(
    Format("<b>{hotel.name}</b>\n"),
    Format("Цена номера: от {hotel.min_price} ₽\n"),
    Format(
        text="{hotel.description}",
        when=F["hotel"].description,
    ),
    Format(
        text="\nИспользуй промокод <b>{hotel.promo_code}</b> "
             "для бронирования и получи скидку!",
        when=F["hotel"].promo_code,
    ),

    Group(
        Url(
            text=Const("Сайт 🌐"),
            url=Format("{hotel.site_url}"),
            id="site_url",
            when=F["hotel"].site_url
        ),
    ),
    buttons.BACK,
    getter=hotel_getter,
    state=HotelSG.hotel
)
