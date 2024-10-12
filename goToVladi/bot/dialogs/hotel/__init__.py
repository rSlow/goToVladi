from aiogram_dialog import Dialog

from .categories import district_window, list_hotels_window
from .hotel import hotel_window

hotels_dialog = Dialog(
    district_window,
    list_hotels_window,
    hotel_window
)
