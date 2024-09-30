from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states import FSMSingleFactory

MainMenuSG = FSMSingleFactory("MainMenuSG", "start")


class RegionSG(StatesGroup):
    start = State()
    set = State()
