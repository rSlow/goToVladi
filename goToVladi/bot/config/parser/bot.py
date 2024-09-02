from typing import Any

from adaptix import Retort

from ..models.bot import BotConfig


def load_bot_config(data: dict[str, Any], retort: Retort) -> BotConfig:
    return retort.load(data, BotConfig)
