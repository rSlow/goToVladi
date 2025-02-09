from aiogram import Router

from .categories import category_sea_recreation_dialog
from .card import sea_recreation_card_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        category_sea_recreation_dialog,
        sea_recreation_card_dialog
    )
    return router
