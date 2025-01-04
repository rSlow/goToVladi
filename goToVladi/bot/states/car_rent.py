from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import FSMSingleFactory


class CarRentSG(StatesGroup):
    category = State()
    rent_list = State()


CarRentCardSG = FSMSingleFactory("CarRentCardSG")
