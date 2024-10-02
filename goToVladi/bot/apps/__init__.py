import logging

from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs as setup_aiogram_dialogs

from goToVladi.bot.config.models.bot import BotConfig
from . import base, hotels, trips
from . import restaurants
from .base.handlers import error

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    error.setup(dp, bot_config.log_chat)

    dp.include_routers(base.handlers.setup())
    # dp.include_routers(restaurants.handlers.setup())

    dp.include_routers(setup_dialogs())
    bg_manager_factory = setup_aiogram_dialogs(dp)

    logger.debug("handlers configured successfully")

    return bg_manager_factory


def setup_dialogs():
    dialogs_router = Router(name=__name__ + ".dialogs")

    dialogs_router.include_router(base.dialogs.setup())
    # dialogs_router.include_router(admin.dialogs.setup())

    dialogs_router.include_router(restaurants.dialogs.setup())
    dialogs_router.include_router(hotels.dialogs.setup())
    dialogs_router.include_router(trips.dialogs.setup())

    logger.debug("dialogs configured successfully")
    return dialogs_router
