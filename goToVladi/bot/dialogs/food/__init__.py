from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.states.food import FoodCategorisesSG, RestaurantListSG, DeliveryListSG, \
    BarListSG, BreakfastListSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types.db_text import DBText
from . import restaurant, delivery, bar, breakfast

food_categories_dialog = Dialog(
    Window(
        DBText("food_start"),
        Group(
            Start(
                text=Const("🍜 Рестораны"),
                id="restaurants",
                state=RestaurantListSG.cuisines
            ),
            Start(
                text=Const("📦 Доставка еды"),
                id="deliveries",
                state=DeliveryListSG.cuisines
            ),
            Start(
                text=Const("🥤 Бары"),
                id="bars",
                state=BarListSG.state
            ),
            Start(
                text=Const("🍳 Завтраки"),
                id="breakfasts",
                state=BreakfastListSG.state
            ),
            width=2,
        ),
        buttons.CANCEL,
        state=FoodCategorisesSG.state
    )
)


def setup():
    router = Router(name=__name__)
    router.include_routers(
        food_categories_dialog,
        restaurant.setup(),
        delivery.setup(),
        bar.setup(),
        breakfast.setup(),
    )
    return router
