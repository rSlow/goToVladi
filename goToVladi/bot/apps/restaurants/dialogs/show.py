from operator import attrgetter

from aiogram import types, F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup, Group, Url, \
    PrevPage, CurrentPage, NextPage, Row, StubScroll
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.restaurants.states import RestaurantSG
from goToVladi.bot.utils import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder


async def get_cuisines(dao: DaoHolder, **__):
    cuisines = await dao.restaurant.get_all_cuisines()
    return {"cuisines": cuisines}


async def set_cuisine(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, cuisine_id: str
):
    manager.dialog_data["cuisine_id"] = int(cuisine_id)
    await manager.next()


cuisine_window = Window(
    Const("Выберите тип кухни:"),
    Select(
        Format("{item.name}"),
        id="cuisines",
        item_id_getter=dto.id_getter,
        items="cuisines",
        on_click=set_cuisine
    ),
    buttons.CANCEL,
    state=RestaurantSG.cuisines,
    getter=get_cuisines
)


async def get_restaurant_types(**__):
    return {"restaurant_types": dto.RestaurantType}


async def set_restaurant_type(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, restaurant_type_name: str
):
    manager.dialog_data["restaurant_type"] = restaurant_type_name
    await manager.next()


type_restaurant_window = Window(
    Const("Выберите вид ресторана:"),
    Select(
        Format("{item.hint}"),
        id="restaurant_types",
        item_id_getter=attrgetter("name"),
        items="restaurant_types",
        on_click=set_restaurant_type
    ),
    buttons.BACK,
    state=RestaurantSG.type_,
    getter=get_restaurant_types
)


async def get_restaurants(dao: DaoHolder, dialog_manager: DialogManager, **__):
    cuisine_id = dialog_manager.dialog_data["cuisine_id"]
    restaurant_type = dialog_manager.dialog_data["restaurant_type"]
    restaurants = await dao.restaurant.get_all(
        cuisine_id=cuisine_id,
        type_=restaurant_type
    )
    return {"restaurants": restaurants}


async def on_restaurant_click(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, restaurant_id: str
):
    manager.dialog_data["restaurant_id"] = int(restaurant_id)
    await manager.next()


restaurants_window = Window(
    Const("Выберите ресторан:"),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            item_id_getter=dto.id_getter,
            id="restaurants",
            items="restaurants",
            on_click=on_restaurant_click,
        ),
        id="restaurants_scroll",
        width=1,
        height=3,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=RestaurantSG.restaurants,
    getter=get_restaurants
)

PHOTOS_SCROLL = "photos_scroll"


async def get_restaurant(dao: DaoHolder, dialog_manager: DialogManager, **__):
    restaurant_id = dialog_manager.dialog_data["restaurant_id"]
    restaurant = await dao.restaurant.get(restaurant_id)
    scroll: ManagedScroll = dialog_manager.find(PHOTOS_SCROLL)
    current_page = await scroll.get_page()
    try:
        current_photo = restaurant.photos[current_page]
    except IndexError:
        current_photo = restaurant.photos[0]
        await scroll.set_page(0)
    return {
        "restaurant": restaurant,
        "photos_count": len(restaurant.photos),
        "current_page": current_page + 1,
        "current_photo_url": current_photo.url
    }


restaurant_window = Window(
    Format("<b>{restaurant.name}</b>\n"),
    Format("<u>Оценка</u>: {restaurant.rating} / 5 ⭐️"),
    Format("<u>Средний чек</u>: {restaurant.average_check} ₽\n"),
    Format(
        text="{restaurant.description}\n",
        when=F["restaurant"].description
    ),
    Format(
        text="<u>Телефон:</u> <code>{restaurant.phone}</code>",
        when=F["restaurant"].phone
    ),
    StubScroll(id=PHOTOS_SCROLL, pages="photos_count"),
    StaticMedia(
        path=Format("{current_photo_url}"),
        type=ContentType.PHOTO,
        when=F["restaurant"].photos
    ),
    Row(
        PrevPage(scroll=PHOTOS_SCROLL, text=Format("◀️")),
        CurrentPage(
            scroll=PHOTOS_SCROLL,
            text=Format("Фото {current_page1} / {pages}")
        ),
        NextPage(scroll=PHOTOS_SCROLL, text=Format("▶️")),
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
    getter=get_restaurant
)

show_dialog = Dialog(
    cuisine_window,
    type_restaurant_window,
    restaurants_window,
    restaurant_window,
)
