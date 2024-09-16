from aiogram_dialog.dialog import Dialog

from .categories import cuisine_window, type_restaurant_window, \
    restaurants_window
from .restraunts import restaurant_window

show_dialog = Dialog(
    cuisine_window,
    type_restaurant_window,
    restaurants_window,
    restaurant_window,
)
