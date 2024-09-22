from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from goToVladi.bot.views.admin_factory import AdminSGFactory
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.data.db.dao.base import BaseDAO


def get_list_admin_dialog(
        admin_states_group: AdminSGFactory, dao_name: str, search_field: str,
        admin_dto:AdminDTO
) -> Dialog:
    async def list_window_getter(dao: DaoHolder, **__):
        app_dao: BaseDAO = getattr(dao, dao_name)

    async def search(
            message: types.Message, widget: ManagedTextInput[str],
            dialog_manager: DialogManager, data: str
    ):
        ...

    return Dialog(
        Window(
            Format("Выберите элемент или введите имя :"),
            ScrollingGroup(
                Select(
                    text=Format("{item.name}"),
                    item_id_getter=dto.id_getter,
                    id="restaurants",
                    items="restaurants",
                    on_click=on_restaurant_click,
                ),
            ),
            TextInput(
                id="search",
                on_success=search
            ),
            state=admin_states_group.list,
        )
    )
