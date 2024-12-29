from aiogram.fsm.state import StatesGroup, State


class SpaSG(StatesGroup):
    spa_list = State()
    spa_card = State()
