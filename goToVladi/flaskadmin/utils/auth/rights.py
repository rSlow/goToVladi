from goToVladi.core.data.db import dto
from goToVladi.core.utils.roles import is_user_has_accessible_role


def has_admin_panel_rights(user: dto.User):
    admin_panel_rights = [
        "creator",
        "admin",
    ]

    return user.is_active \
        and is_user_has_accessible_role(user, admin_panel_rights, allow_superuser=True)


def is_admin_panel_user(user: dto.User):
    return user.is_authenticated and has_admin_panel_rights(user)


def is_superuser(user: dto.User):
    return user.is_authenticated \
        and user.is_active \
        and user.is_superuser
