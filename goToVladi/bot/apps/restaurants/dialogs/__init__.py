from aiogram import Router

from .show import restaurants_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(restaurants_dialog)

    return router
