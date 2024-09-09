from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.base.states import MainMenuSG
from goToVladi.bot.apps.restaurants.states import RestaurantSG

main_menu = Dialog(
    Window(
        Const("Добро пожаловать в бот GoToVladi!"),
        Const("Выберите категорию:"),
        Start(
            Const("Рестораны"),
            id="restaurants",
            state=RestaurantSG.cuisines
        ),
        state=MainMenuSG.state
    )
)
