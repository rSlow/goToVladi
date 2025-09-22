from typing import Any, Callable, Optional, Awaitable, ParamSpec

from dishka import AsyncContainer

from goToVladi.core.data.db.dao import SettingsDao

P = ParamSpec("P")


def db_settings_filter(
        key: str, allowed_value: Any = True,
        worker: Optional[Callable[P, Awaitable[bool]]] = None
):
    async def _db_settings_filter(*args, **kwargs):
        container: AsyncContainer = kwargs.get("dishka_container")
        settings_dao = await container.get(SettingsDao)
        setting = await settings_dao.get_by_key(key)
        if setting is None:
            return True

        setting_value = setting.value
        if setting_value.isdigit():
            setting_value = int(setting_value)

        if allowed_value is True:
            setting_value = bool(setting_value)

        is_filter_allowed = setting_value == allowed_value

        if worker is not None and not is_filter_allowed:
            return await worker(*args, **kwargs)

        return is_filter_allowed

    return _db_settings_filter
