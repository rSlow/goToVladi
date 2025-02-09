from aiogram.fsm.state import StatesGroup, State


class CooperationSG(StatesGroup):
    input = State()
    contact = State()
