from aiogram import Router

from .card import breakfast_card_dialog
from .categories import category_breakfast_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        category_breakfast_dialog,
        breakfast_card_dialog
    )
    return router
