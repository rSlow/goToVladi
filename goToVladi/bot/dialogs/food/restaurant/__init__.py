from aiogram import Router

from .card import restaurant_card_dialog
from .categories import restaurant_list_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        restaurant_list_dialog,
        restaurant_card_dialog
    )
    return router
