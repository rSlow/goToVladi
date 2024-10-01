from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.apps.base.states import MainMenuSG, RegionSG
from goToVladi.bot.apps.hotels.states import HotelSG
from goToVladi.bot.apps.restaurants.states import RestaurantSG

has_region = F["middleware_data"]["user"].region.is_not(None)

main_menu = Dialog(
    Window(
        Const(
            "Выберите категорию:",
            when=has_region
        ),
        Group(
            Start(
                text=Const("Рестораны"),
                id="restaurants",
                state=RestaurantSG.cuisines
            ),
            Start(
                text=Const("Отели"),
                id="hotels",
                state=HotelSG.district,
            ),
            when=has_region
        ),

        Const(
            "Регион поиска не установлен. Нажмите кнопку 'Установить регион'.",
            when=~has_region
        ),
        Start(
            text=Const("Установить регион"),
            id="set_region",
            state=RegionSG.set,
            when=~has_region
        ),
        state=MainMenuSG.state
    )
)
