from aiogram import Router
from aiogram.filters import Command

from bot.views.commands import START_COMMAND
from .start import start


def setup():
    router = Router(name=__name__)
    router.message.register(start, Command(START_COMMAND))

    return router
