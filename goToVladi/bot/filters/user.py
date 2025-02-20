from typing import cast, Iterable

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from magic_filter import MagicFilter

from goToVladi.bot.filters.base import F_MD
from goToVladi.core.data.db import dto

F_User = cast(MagicFilter, F_MD["user"])


def _check_user(user: dto.User, role_names: Iterable[str], allow_superuser: bool):
    if allow_superuser and user.is_superuser:
        return True
    for role_name in role_names:
        if role_name in user.roles:
            return True
    return False


def adg_role_filter(*role_names: str, allow_superuser: bool = True):
    def _adg_role_filter(_data: dict, _widget: Whenable, manager: DialogManager):
        user: dto.User = manager.middleware_data["user"]
        return _check_user(user, role_names, allow_superuser)

    return _adg_role_filter


def role_filter(*role_names: str, allow_superuser: bool = True):
    def _role_filter(_msg: types.Message, user: dto.User, **__) -> bool:
        return _check_user(user, role_names, allow_superuser)

    return _role_filter
