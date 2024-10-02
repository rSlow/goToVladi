from aiogram import Router

from .show import trips_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(trips_dialog)

    return router
