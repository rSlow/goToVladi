from aiogram_dialog import Dialog

from dialog_schematic_manager import with_schematic, DataParam
from .card import hotel_window
from .categories import district_window, list_hotels_window

hotels_dialog = Dialog(
    with_schematic(
        district_window,
        alias="Отели: выбор района"
    ),

    list_hotels_window,

    with_schematic(
        hotel_window,
        alias="Карточка отеля",
        dialog_data=[DataParam(
            param_name="hotel_id",
            param_alias="Отель"
        )]
    ),
)
