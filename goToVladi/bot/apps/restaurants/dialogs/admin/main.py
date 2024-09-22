from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.restaurants.states import AdminRestaurantSG
from goToVladi.bot.utils import buttons
from goToVladi.core.data.db.dao import DaoHolder


async def admin_restaurant_getter(dao: DaoHolder, **__):
    restaurants_count = await dao.restaurant.count()
    return {"restaurants_count": restaurants_count}


admin_restaurant_dialog = Dialog(
    Window(
        Format("Всего ресторанов: {restaurants_count}"),
        SwitchTo(
            Const("Список ресторанов"),
            id="list",
            state=AdminRestaurantSG.list
        ),
        SwitchTo(
            Const("Добавить ресторан"),
            id="add",
            state=AdminRestaurantSG.add
        ),
        buttons.CANCEL,
        state=AdminRestaurantSG.main,
        getter=admin_restaurant_getter
    )
)
