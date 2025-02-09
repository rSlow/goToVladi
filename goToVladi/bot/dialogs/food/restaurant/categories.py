from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import RestaurantListSG, RestaurantCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.scrolls.scrolling_group import ScrollingGroup
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import RestaurantDao


@inject
async def get_cuisines(dao: FromDishka[RestaurantDao], user: dto.User, **__):
    cuisines = await dao.get_all_cuisines(region_id=user.region.id)
    return {"cuisines": cuisines}


async def set_cuisine(_, __, manager: DialogManager, cuisine_id: str):
    manager.dialog_data["cuisine_id"] = int(cuisine_id)
    await manager.next()


cuisines_window = Window(
    Const(
        "Выберите тип кухни:",
        when=F["cuisines"]
    ),
    Format(
        "К сожалению, в <b>{region.name}</b> мы еще не добавили рестораны. Скоро добавим!",
        when=~F["cuisines"]
    ),

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
    state=RestaurantListSG.cuisines,
    getter=get_cuisines
)


@inject
async def get_restaurants(
        dao: FromDishka[RestaurantDao], dialog_manager: DialogManager, user: dto.User, **__
):
    cuisine_id = dialog_manager.dialog_data["cuisine_id"]
    restaurants = await dao.get_filtered_list(cuisine_id=cuisine_id, region_id=user.region.id)
    return {"restaurants": restaurants}


async def on_restaurant_click(_, __, manager: DialogManager, restaurant_id: str):
    await manager.start(RestaurantCardSG.state, data={"restaurant_id": int(restaurant_id)})


restaurants_window = Window(
    Const(
        "Выберите ресторан:",
        when=F["restaurants"]
    ),
    Const(
        f"В данной категории пока нет ресторанов, "
        f"но мы обязательно скоро добавим!",
        when=~F["restaurants"]
    ),
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
    state=RestaurantListSG.restaurant_list,
    getter=get_restaurants
)

restaurant_list_dialog = Dialog(
    cuisines_window,
    restaurants_window
)
