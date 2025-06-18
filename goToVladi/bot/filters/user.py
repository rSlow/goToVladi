from typing import cast

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from magic_filter import MagicFilter

from goToVladi.bot.filters.base import F_MD
from goToVladi.core.data.db import dto
from goToVladi.core.utils.roles import is_user_has_accessible_role

F_User = cast(MagicFilter, F_MD["user"])


def adg_role_filter(*role_names: str, allow_superuser: bool = True):
    def _adg_role_filter(_data: dict, _widget: Whenable, manager: DialogManager):
        user: dto.User = manager.middleware_data["user"]
        return is_user_has_accessible_role(user, role_names, allow_superuser)

    return _adg_role_filter


def role_filter(*role_names: str, allow_superuser: bool = True):
    def _role_filter(_msg: types.Message, user: dto.User, **__) -> bool:
        return is_user_has_accessible_role(user, role_names, allow_superuser)

    return _role_filter
