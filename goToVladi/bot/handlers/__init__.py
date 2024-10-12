import logging

from aiogram import Dispatcher

from goToVladi.bot.config.models.bot import BotConfig
from . import commands
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    errors.setup(dp, bot_config.log_chat)

    dp.include_routers(commands.setup())

    logger.debug("handlers configured successfully")
