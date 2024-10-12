from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.states.hotel import HotelSG
from goToVladi.bot.states.region import RegionSG
from goToVladi.bot.states.restaurant import RestaurantSG
from goToVladi.bot.states.start import MainMenuSG
from goToVladi.bot.states.trip import TripSG

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
            Start(
                text=Const("Экскурсии"),
                id="trips",
                state=TripSG.trip_list,
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
