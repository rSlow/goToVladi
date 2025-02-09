from aiogram import Router

from .categories import category_massage_dialog
from .card import massage_card_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        category_massage_dialog,
        massage_card_dialog
    )
    return router
