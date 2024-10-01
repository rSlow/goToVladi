from aiogram import Router

from .main_menu import main_menu
from .region import region_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(main_menu)
    router.include_router(region_dialog)

    return router
