import logging

from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs as setup_aiogram_dialogs

from goToVladi.bot.config.models.bot import BotConfig
from . import base
from . import restaurants
from .base.handlers import error

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    error.setup(dp, bot_config.log_chat)

    dp.include_routers(base.handlers.setup())
    dp.include_routers(restaurants.handlers.setup())

    setup_dialogs(dp)

    logger.debug("handlers configured successfully")


def setup_dialogs(router: Router):
    dialogs_router = Router(name=__name__ + ".dialogs")

    dialogs_router.include_router(restaurants.dialogs.setup())

    setup_aiogram_dialogs(dialogs_router)
    router.include_router(dialogs_router)

    logger.debug("dialogs configured successfully")
