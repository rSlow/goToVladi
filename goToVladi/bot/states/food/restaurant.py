__all__ = [
    "RestaurantListSG",
    "RestaurantCardSG",
]

from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import FSMSingleFactory


class RestaurantListSG(StatesGroup):
    cuisines = State()
    restaurant_list = State()


RestaurantCardSG = FSMSingleFactory("RestaurantCardSG")
