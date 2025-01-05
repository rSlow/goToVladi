from aiogram import Router

from .categoring import car_rent_category_dialog
from .car_rent import car_rent_dialog


def setup():
    router = Router(name=__name__)
    router.include_routers(
        car_rent_category_dialog,
        car_rent_dialog
    )
    return router
