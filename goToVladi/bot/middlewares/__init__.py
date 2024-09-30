from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory

from .additional_message import AdditionalMessageMiddleware
from .context_data import ContextDataMiddleware
from .region import RegionMiddleware


def setup_middlewares(dp: Dispatcher, bg_manager_factory: BgManagerFactory):
    dp.update.middleware(
        ContextDataMiddleware(bg_manager_factory=bg_manager_factory)
    )

    additional_message_middleware = AdditionalMessageMiddleware()
    dp.message.middleware(additional_message_middleware)
    dp.business_message.middleware(additional_message_middleware)
    dp.callback_query.middleware(additional_message_middleware)

    # dp.update.middleware(RegionMiddleware())
