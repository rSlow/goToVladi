__all__ = [
    "DeliveryListSG",
    "DeliveryCardSG",
]

from aiogram.fsm.state import StatesGroup, State

from goToVladi.bot.utils.states_factory import FSMSingleFactory


class DeliveryListSG(StatesGroup):
    cuisines = State()
    delivery_list = State()


DeliveryCardSG = FSMSingleFactory("DeliveryCardSG")
