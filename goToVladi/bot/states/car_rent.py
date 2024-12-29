from aiogram.fsm.state import StatesGroup, State


class CarRentSG(StatesGroup):
    category = State()
    rent_list = State()
    rent_card = State()
