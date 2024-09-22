from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.admin.states import AdminMainSG
from goToVladi.bot.views.admin_factory import get_admin_dialog


def setup_admin_apps(*apps: Start):
    restaurants_admin_dialog = get_admin_dialog(
        app_name="restaurants",
        dao_name="restaurant"
    )

    main_admin_dialog = Dialog(
        Window(
            Const("Выберите категорию:"),
            Start(
                text=Const("Рестораны"),
                id="restaurants",
                state=restaurants_admin_dialog.main_state
            ),
            state=AdminMainSG.state
        )
    )

    return main_admin_dialog
