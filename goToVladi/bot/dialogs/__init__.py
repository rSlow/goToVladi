import logging

from aiogram import Router, Dispatcher
from aiogram_dialog import setup_dialogs as setup_aiogram_dialogs

from . import massage, car_rent, food, sea_recreation
from .cooperation import cooperation_dialog
from .hotel import hotels_dialog
from .main_menu import main_menu
from .region import region_dialog
from .trip import trips_dialog

logger = logging.getLogger(__name__)


def setup_dialogs(dp: Dispatcher):
    dialog_router = Router(name=__name__)

    dialog_router.include_router(main_menu)
    dialog_router.include_router(region_dialog)

    dialog_router.include_router(food.setup())
    dialog_router.include_router(hotels_dialog)
    dialog_router.include_router(trips_dialog)
    dialog_router.include_router(massage.setup())
    dialog_router.include_router(car_rent.setup())
    dialog_router.include_router(sea_recreation.setup())

    dialog_router.include_router(cooperation_dialog)

    dp.include_router(dialog_router)

    bg_manager_factory = setup_aiogram_dialogs(dp)
    logger.debug("dialogs configured successfully")

    return bg_manager_factory
