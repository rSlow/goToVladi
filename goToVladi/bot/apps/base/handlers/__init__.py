from aiogram import Router

from . import commands


def setup():
    router = Router(name=__name__)

    router.include_router(commands.setup())

    return router
