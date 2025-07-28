from enum import StrEnum, auto
from typing import Any, Callable, Optional, Awaitable, ParamSpec, final

from dishka import AsyncContainer

from goToVladi.bot.views.alert import BotAlert
from goToVladi.core.data.db.dao import SettingsDao

P = ParamSpec("P")


@final
class MatchMode(StrEnum):
    allow_if_matched = auto()
    allow_if_not_matched = auto()


def filter_on_db_setting(
        key: str, value_to_filter_work: Any = True,
        match_mode: MatchMode = MatchMode.allow_if_not_matched,
        filter_: Optional[Callable[P, Awaitable[bool]]] = None
):
    async def _filter_on_db_setting(*args, **kwargs):
        container: AsyncContainer = kwargs.get("dishka_container")
        settings_dao = await container.get(SettingsDao)
        setting = await settings_dao.get_by_key(key)
        if setting is None:
            alert = await container.get(BotAlert)
            await alert(f"setting {key = } is not found!")
            return match_mode == MatchMode.allow_if_not_matched

        db_value = setting.value
        if db_value.isdigit():
            db_value = int(db_value)

        if value_to_filter_work is True:
            db_value = bool(db_value)

        values_matched = db_value == value_to_filter_work
        if values_matched and filter_ is not None:
            return await filter_(*args, **kwargs)

        if match_mode is MatchMode.allow_if_matched:
            return values_matched

        if match_mode is MatchMode.allow_if_not_matched:
            return not values_matched

        return False

    return _filter_on_db_setting
