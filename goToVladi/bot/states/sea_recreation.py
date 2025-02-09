from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import FSMSingleFactory


class SeaRecreationListSG(StatesGroup):
    category = State()
    sea_recreation_list = State()


SeaRecreationCardSG = FSMSingleFactory("SeaRecreationCardSG")
