from aiogram import Dispatcher, BaseMiddleware
from aiogram_dialog import BgManagerFactory

from .additional_message import AdditionalMessageMiddleware
from .context_data import ContextDataMiddleware
from .logging import EventLoggingMiddleware


def setup_middlewares(dp: Dispatcher, bg_manager_factory: BgManagerFactory):
    dp.update.middleware(
        ContextDataMiddleware(bg_manager_factory=bg_manager_factory)
    )

    _base_setup_middleware(dp, AdditionalMessageMiddleware())
    _base_setup_middleware(dp, EventLoggingMiddleware())


def _base_setup_middleware(dp: Dispatcher, middleware: BaseMiddleware):
    dp.message.middleware(middleware)
    dp.business_message.middleware(middleware)
    dp.callback_query.middleware(middleware)
