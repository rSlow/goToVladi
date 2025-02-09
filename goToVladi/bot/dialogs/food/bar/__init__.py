from aiogram import Router

from .card import bar_card_dialog
from .categories import category_bar_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        category_bar_dialog,
        bar_card_dialog
    )
    return router
