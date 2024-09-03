from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.base.states import MainMenuSG

main_menu = Dialog(
    Window(
        Const("Добро пожаловать в бот GoToVladi!"),
        state=MainMenuSG.state
    )
)
