from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import FSMSingleFactory


class CarRentSG(StatesGroup):
    car_class = State()
    rent_list = State()


CarRentCardSG = FSMSingleFactory("CarRentCardSG")
