from aiogram.fsm.state import StatesGroup, State


class RestaurantSG(StatesGroup):
    category = State()
    type_ = State()
    average_check = State()
