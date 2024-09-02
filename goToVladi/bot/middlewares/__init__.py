from aiogram import Dispatcher

from .context_data import ContextDataMiddleware


def setup_middlewares(
    dp: Dispatcher,
):
    dp.update.middleware(ContextDataMiddleware())
