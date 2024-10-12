from aiogram_dialog.dialog import Dialog

from .categories import cuisine_window, type_restaurant_window, \
    restaurants_window
from .restraunt import restaurant_window

restaurants_dialog = Dialog(
    cuisine_window,
    type_restaurant_window,
    restaurants_window,
    restaurant_window,
)
