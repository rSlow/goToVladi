from aiogram import Dispatcher
from dishka import Provider, Scope, provide

from bot_schema_parser.schematic import BotSchema
from bot_schema_parser.setup import get_dp_schematic


class BotSchemaProvider(Provider):
    scope = Scope.APP

    @provide
    def get_bot_schema(self, dp: Dispatcher) -> BotSchema:
        return get_dp_schematic(dp)
