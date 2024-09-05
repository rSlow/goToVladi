from operator import itemgetter as ig

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.restaurants.states import RestaurantSG
from goToVladi.core.data.db.dao import DaoHolder


async def get_cuisines(dao: DaoHolder, **__):
    cuisines = dao.restaurant.get_all_cuisines()
    return {"cuisines": cuisines}


category_window = Window(
    Const("Выберите тип кухни:"),
    Select(
        Format("{item[0]}"),
        id="devices",
        item_id_getter=lambda x: x.id_,
        items="devices",
        on_click=set_device
    ),
    state=RestaurantSG.category,
    getter=get_cuisines
)

show_dialog = Dialog(
    category_window,
)
