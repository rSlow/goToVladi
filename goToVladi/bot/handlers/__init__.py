import logging

from aiogram import Dispatcher, Router

from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.filters.private import set_chat_private_filter
from . import base_commands
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    errors.setup(dp, bot_config.log_chat)

    handlers_router = Router(name=__name__)
    set_chat_private_filter(handlers_router)

    handlers_router.include_routers(
        base_commands.setup(),
    )
    dp.include_router(handlers_router)

    logger.debug("handlers configured successfully")
