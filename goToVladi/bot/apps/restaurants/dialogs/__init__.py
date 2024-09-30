from aiogram import Router

from .show import show_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(show_dialog)

    return router
