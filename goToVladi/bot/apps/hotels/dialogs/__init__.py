from aiogram import Router

from .show import hotels_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(hotels_dialog)

    return router
