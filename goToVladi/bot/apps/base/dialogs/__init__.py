from aiogram import Router

from .main_menu import main_menu


def setup():
    router = Router(name=__name__)
    router.include_router(main_menu)

    return router
