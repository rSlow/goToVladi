from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll as MScroll
from aiogram_dialog.widgets.kbd import Group, Url, \
    PrevPage, CurrentPage, NextPage, Row, StubScroll
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.restaurants.states import RestaurantSG
from goToVladi.bot.utils import buttons
from goToVladi.bot.utils.scroll import normalize_scroll
from goToVladi.bot.views.types.scrolling_n_text import ScrollingSplitText, \
    PageTable
from goToVladi.core.data.db.dao import DaoHolder

PHOTOS_SCROLL = "photos_scroll"
DESCRIPTION_SCROLL = "description_scroll"


async def get_restaurant(dao: DaoHolder, dialog_manager: DialogManager, **__):
    restaurant_id = dialog_manager.dialog_data["restaurant_id"]
    restaurant = await dao.restaurant.get(restaurant_id)

    photos_scroll: MScroll = dialog_manager.find(PHOTOS_SCROLL)
    await normalize_scroll(restaurant.photos, photos_scroll)

    if restaurant.description:
        description_scroll: MScroll = dialog_manager.find(DESCRIPTION_SCROLL)
        await normalize_scroll(
            PageTable(restaurant.description, 600, "\n").pages,
            description_scroll
        )

    current_photo_page = await photos_scroll.get_page()
    current_photo = restaurant.photos[current_photo_page]

    return {
        "restaurant": restaurant,
        "photos_count": len(restaurant.photos),
        "description_length": (
            len(restaurant.description)
            if restaurant.description else 0
        ),
        "current_page": current_photo_page + 1,
        "current_photo_url": current_photo.url
    }


restaurant_window = Window(
    Format("<b>{restaurant.name}</b>\n"),
    Format("<u>Оценка</u>: {restaurant.rating} / 5 ⭐️"),
    Format("<u>Средний чек</u>: {restaurant.average_check} ₽\n"),

    ScrollingSplitText(
        text=Format("{restaurant.description}"),
        id_=DESCRIPTION_SCROLL,
        page_size=600,
        when=F["restaurant"].description,
        splitter="\n"
    ),
    Row(
        PrevPage(
            id=DESCRIPTION_SCROLL + "_prev",
            scroll=DESCRIPTION_SCROLL, text=Format("◀️")
        ),
        CurrentPage(
            id=DESCRIPTION_SCROLL + "_current", scroll=DESCRIPTION_SCROLL,
            text=Format("Описание {current_page1} / {pages}")
        ),
        NextPage(
            id=DESCRIPTION_SCROLL + "_next",
            scroll=DESCRIPTION_SCROLL, text=Format("▶️")
        ),
        when=F["description_length"] > 900
    ),

    Format(
        text="<u>\nТелефон:</u> <code>{restaurant.phone}</code>",
        when=F["restaurant"].phone
    ),

    StubScroll(id=PHOTOS_SCROLL, pages="photos_count"),
    StaticMedia(
        path=Format("{current_photo_url}"),
        type=ContentType.PHOTO,
        when=F["restaurant"].photos
    ),
    Row(
        PrevPage(
            id=PHOTOS_SCROLL + "_prev",
            scroll=PHOTOS_SCROLL, text=Format("◀️")
        ),
        CurrentPage(
            id=PHOTOS_SCROLL + "_current", scroll=PHOTOS_SCROLL,
            text=Format("Фото {current_page1} / {pages}")
        ),
        NextPage(
            id=PHOTOS_SCROLL + "_next",
            scroll=PHOTOS_SCROLL, text=Format("▶️")
        ),
        when=F["photos_count"] > 1
    ),

    Group(
        Url(
            text=Const("Сайт 🌐"),
            url=Format("{restaurant.site_url}"),
            id="site_url",
            when=F["restaurant"].site_url
        ),
        Url(
            text=Const("WhatsApp"),
            url=Format("{restaurant.whatsapp}"),
            id="whatsapp",
            when=F["restaurant"].whatsapp
        ),
        Url(
            text=Const("Instagram"),
            url=Format("{restaurant.instagram}"),
            id="instagram",
            when=F["restaurant"].instagram
        ),
        Url(
            text=Const("VK"),
            url=Format("{restaurant.vk}"),
            id="vk",
            when=F["restaurant"].vk
        ),
        Url(
            text=Const("Telegram"),
            url=Format("{restaurant.telegram}"),
            id="telegram",
            when=F["restaurant"].telegram
        ),
        width=2
    ),
    buttons.BACK,
    state=RestaurantSG.restaurant,
    getter=get_restaurant,
)
