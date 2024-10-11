from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.views.admin_factory import AdminSGFactory
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.data.db.dao.base import BaseDao


def get_main_admin_dialog(
        admin_states_group: AdminSGFactory, dao_name: str
) -> Dialog:
    async def main_window_getter(dao: DaoHolder, **__):
        app_dao: BaseDao = getattr(dao, dao_name)
        count = await app_dao.count()
        return {"count": count}

    return Dialog(
        Window(
            Format("Всего элементов: {count}"),

            SwitchTo(
                Const("Список"),
                id="list",
                state=admin_states_group.list
            ),
            SwitchTo(
                Const("Добавить"),
                id="add",
                state=admin_states_group.add
            ),
            state=admin_states_group.main,
            getter=main_window_getter
        )
    )
