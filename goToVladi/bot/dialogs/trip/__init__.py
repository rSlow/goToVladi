from aiogram_dialog import Dialog

from .categories import list_trips_window
from .card import trip_window

trips_dialog = Dialog(
    list_trips_window,
    trip_window
)
