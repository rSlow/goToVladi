from operator import itemgetter

from aiogram import types
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup, Group
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
    Group(
        Select(
            Format("{item.name}"),
            id="cuisines",
            item_id_getter=dto.id_getter,
            items="cuisines",
            on_click=set_cuisine
        ),
        width=3
    ),
    buttons.CANCEL,
    state=RestaurantSG.cuisines,
    getter=get_cuisines
)


async def get_restaurant_types(**__):
    return {
        "restaurant_types": [
            ("delivery", "Доставка"),
            ("inner", "На месте"),
        ]
    }


async def set_restaurant_type(
        _: types.CallbackQuery, __: Select,
        manager: DialogManager, restaurant_type: str
):
    manager.dialog_data["restaurant_type"] = restaurant_type
    await manager.next()


type_restaurant_window = Window(
    Const("Выберите вид ресторана:"),
    Select(
        Format("{item[1]}"),
        id="restaurant_types",
        item_id_getter=itemgetter(0),
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
    is_delivery = restaurant_type == "delivery"
    is_inner = restaurant_type == "inner"
    restaurants = await dao.restaurant.get_all(
        cuisine_id=cuisine_id,
        is_inner=is_inner,
        is_delivery=is_delivery
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
