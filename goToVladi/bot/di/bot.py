import logging
from typing import AsyncIterable, NewType

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from dishka import Provider, Scope, provide, from_context

from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.config.models.main import BotAppConfig
from goToVladi.bot.config.models.storage import StorageConfig
from goToVladi.bot.views import commands
from goToVladi.bot.views.alert import BotAlert

BotCommandsList = NewType('CommandsList', list[BotCommand])

logger = logging.getLogger(__name__)


class BotProvider(Provider):
    scope = Scope.APP

    bot_config = from_context(BotAppConfig)

    @provide
    def get_bot_config(self, config: BotAppConfig) -> BotConfig:
        return config.bot

    @provide
    def get_bot_storage_config(self, config: BotAppConfig) -> StorageConfig:
        return config.storage

    @provide
    async def get_common_commands(self) -> BotCommandsList:
        return BotCommandsList([
            commands.START,
            commands.HELP,
            commands.ABOUT,
            commands.UPDATE,
            commands.REGION,
        ])

    @provide
    async def get_bot(
            self, bot_config: BotConfig, bot_commands: BotCommandsList
    ) -> AsyncIterable[Bot]:
        bot = Bot(
            token=bot_config.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, allow_sending_without_reply=True
            )
        )
        await bot.set_my_commands(
            commands=bot_commands,
            scope=BotCommandScopeAllPrivateChats()
        )
        yield bot
        await bot.session.close()

    @provide
    async def bot_alert(self, bot: Bot, bot_config: BotConfig) -> BotAlert:
        return BotAlert(bot, bot_config.log_chat)
