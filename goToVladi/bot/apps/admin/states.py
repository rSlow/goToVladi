from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import SGSingleFactory

AdminMainSG = SGSingleFactory("AdminMainSG")


class MailingSG(StatesGroup):
    text = State()
    approve = State()
