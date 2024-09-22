from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group

from goToVladi.bot.apps.restaurants.states import AdminRestaurantSG

add_admin_restaurant_window = Dialog(
    Window(
        Group(

            width=2
        ),
        state=AdminRestaurantSG.add
    )
)
