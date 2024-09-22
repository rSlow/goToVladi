__all__ = [
    "RestaurantSG",
    "AdminRestaurantSG"
]

from aiogram.fsm.state import StatesGroup, State


class RestaurantSG(StatesGroup):
    cuisines = State()
    type_ = State()
    restaurants = State()
    restaurant = State()


class AdminRestaurantSG(StatesGroup):
    main = State()
    list = State()
    add = State()
    delete = State()
    edit = State()
