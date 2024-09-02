import logging

from aiogram import Dispatcher

from goToVladi.bot.config.models.bot import BotConfig

logger = logging.getLogger(__name__)


# TODO подумать куда переместить

def setup_handlers(
        dp: Dispatcher,
        bot_config: BotConfig
):
    # errors.setup(dp, bot_config.log_chat)
    #
    # dp.include_router(base.setup())
    #
    # dialogs.setup(dp)

    logger.debug("handlers configured successfully")
