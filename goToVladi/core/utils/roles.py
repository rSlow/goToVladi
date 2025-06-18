from typing import Iterable

from goToVladi.core.data.db import dto


def is_user_has_accessible_role(
        user: dto.User, accessible_role_names: Iterable[str], allow_superuser: bool
):
    if allow_superuser and user.is_superuser:
        return True
    for role_name in accessible_role_names:
        if role_name in user.roles:
            return True
    return False
