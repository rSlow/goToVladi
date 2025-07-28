import logging

from aiogram import Dispatcher
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka as setup_aiogram_dishka

from goToVladi.bot.config.models import BotConfig
from goToVladi.bot.dialogs import setup_dialogs
from goToVladi.bot.filters.base import set_filter_on_router
from goToVladi.bot.filters.db_settings import filter_on_db_setting, MatchMode
from goToVladi.bot.filters.workers import superusers_worker
from goToVladi.bot.handlers import setup_handlers
from goToVladi.bot.middlewares import setup_middlewares
from goToVladi.bot.utils.router import print_router_tree

logger = logging.getLogger(__name__)


def setup_dispatcher(dp: Dispatcher, container: AsyncContainer, bot_config: BotConfig):
    setup_aiogram_dishka(container=container, router=dp)
    setup_handlers(dp, bot_config)
    bg_manager_factory = setup_dialogs(dp)
    setup_middlewares(dp=dp, bg_manager_factory=bg_manager_factory)

    logger.info(
        "Configured bot routers \n%s",
        print_router_tree(dp) + "\n"
    )
    set_filter_on_router(
        dp,
        filter_on_db_setting(
            key="only-admins-visible", value_to_filter_work=1,
            match_mode=MatchMode.allow_if_not_matched,
            filter_=superusers_worker
        )
    )
