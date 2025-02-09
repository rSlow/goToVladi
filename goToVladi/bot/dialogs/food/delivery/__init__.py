from aiogram import Router

from .card import delivery_card_dialog
from .categories import delivery_list_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        delivery_list_dialog,
        delivery_card_dialog
    )
    return router
