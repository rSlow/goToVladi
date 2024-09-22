from dataclasses import dataclass

from aiogram.fsm.state import State
from aiogram_dialog import Dialog

from goToVladi.bot.views.admin_factory.dialogs.list import get_list_admin_dialog
from goToVladi.bot.views.admin_factory.dialogs.main import get_main_admin_dialog
from goToVladi.bot.views.admin_factory.forms import AdminDTO
from goToVladi.bot.views.admin_factory.states_factory import AdminSGFactory


@dataclass
class AdminDialogSchema:
    dialog: Dialog
    main_state: State


def get_admin_dialog(
        app_name: str, dao_name: str, dto: AdminDTO
) -> AdminDialogSchema:
    admin_states_group = AdminSGFactory(app_name)
    main_admin_dialog = get_main_admin_dialog(
        admin_states_group=admin_states_group, dao_name=dao_name
    )
    list_admin_dialog = get_list_admin_dialog(
        admin_states_group=admin_states_group, dao_name=dao_name,
        search_field="name",
    )

    return AdminDialogSchema(
        dialog=main_admin_dialog,
        main_state=admin_states_group.main
    )
