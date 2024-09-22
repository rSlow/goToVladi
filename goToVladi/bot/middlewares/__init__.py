from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory

from .context_data import ContextDataMiddleware


def setup_middlewares(dp: Dispatcher, bg_manager_factory: BgManagerFactory):
    dp.update.middleware(
        ContextDataMiddleware(bg_manager_factory=bg_manager_factory)
    )
