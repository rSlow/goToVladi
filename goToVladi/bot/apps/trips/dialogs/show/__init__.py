from aiogram_dialog import Dialog

from .categories import list_trips_window
from .trip import trip_window

trips_dialog = Dialog(
    list_trips_window,
    trip_window
)
