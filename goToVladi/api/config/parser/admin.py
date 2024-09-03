from typing import Any

from adaptix import Retort, name_mapping, NameStyle

from ..models.admin import AdminConfig


def load_admin_config(dct: dict[str, Any]) -> AdminConfig:
    admin_dct = dct["admin"].copy()
    admin_dct["secret-key"] = dct["auth"]["secret-key"]
    admin_dct = {f"admin-{key}": value for key, value in admin_dct.items()}

    retort = Retort(
        recipe=[name_mapping(name_style=NameStyle.LOWER_KEBAB)]
    )
    return retort.load(admin_dct, AdminConfig)
