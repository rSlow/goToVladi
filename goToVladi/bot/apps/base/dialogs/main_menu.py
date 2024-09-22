from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.base.states import MainMenuSG
from goToVladi.bot.apps.restaurants.states import RestaurantSG
from goToVladi.bot.middlewares.config import MiddlewareData


def is_superuser(data: dict, _: Whenable, __: DialogManager):
    middleware_data: MiddlewareData = data["middleware_data"]
    user = middleware_data["user"]
    superusers = middleware_data["bot_config"].superusers
    return user.tg_id in superusers


main_menu = Dialog(
    Window(
        Const("Добро пожаловать в бот GoToVladi!"),
        Const("Выберите категорию:"),
        Start(
            Const("Рестораны"),
            id="restaurants",
            state=RestaurantSG.cuisines
        ),
        # Start(
        #     Const("Админка"),
        #     id="admin",
        #     state=AdminMainSG.main_state,
        #     when=is_superuser
        # ),
        state=MainMenuSG.state
    )
)
