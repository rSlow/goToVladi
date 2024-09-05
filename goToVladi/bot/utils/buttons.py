from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start, Cancel, Back, Next
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.base.states import MainMenuSG

MAIN_MENU_BUTTON = Start(
    text=Const("Главное меню ☰"),
    id="__main__",
    state=MainMenuSG.state,
    mode=StartMode.RESET_STACK
)

CANCEL_BUTTON = Cancel(
    text=Const("Назад ◀")
)

BACK_BUTTON = Back(
    text=Const("Назад ◀")
)
NEXT_BUTTON = Next(
    text=Const("Вперед ◀")
)
