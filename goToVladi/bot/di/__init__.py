__all__ = [
    "get_bot_providers",
]

from dishka import Provider

from .bot import BotProvider
# from .bot_schema import BotSchemaProvider
from .dp import DpProvider
from .interactors import InteractorProvider
from .jinja import JinjaProvider


def get_bot_providers() -> list[Provider]:
    return [
        BotProvider(),
        # BotSchemaProvider(),
        DpProvider(),
        JinjaProvider(),
        InteractorProvider()
    ]
