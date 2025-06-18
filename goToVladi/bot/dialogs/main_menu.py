from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const

from goToVladi.bot.dialogs.region import has_region
from goToVladi.bot.filters.user import F_User
from goToVladi.bot.states.admin import AdminMainSG
from goToVladi.bot.states.car_rent import CarRentSG
from goToVladi.bot.states.cooperation import CooperationSG
from goToVladi.bot.states.food import FoodCategorisesSG
from goToVladi.bot.states.hotel import HotelSG
from goToVladi.bot.states.massage import MassageListSG
from goToVladi.bot.states.region import RegionSG
from goToVladi.bot.states.sea_recreation import SeaRecreationListSG
from goToVladi.bot.states.start import MainMenuSG
from goToVladi.bot.states.trip import TripSG

main_menu = Dialog(
    Window(
        Const(
            "Выберите категорию:",
            when=has_region
        ),
        Group(
            Start(
                text=Const("🍛 Гид по еде"),
                id="food",
                state=FoodCategorisesSG.state
            ),
            Start(
                text=Const("🏨 Отели"),
                id="hotels",
                state=HotelSG.district,
            ),
            Start(
                text=Const("🌏 Экскурсии"),
                id="trips",
                state=TripSG.trip_list,
            ),
            Start(
                text=Const("🌊 Морской отдых"),
                id="sea_recreation",
                state=SeaRecreationListSG.category,
            ),
            Start(
                text=Const("💆 Спа / массажи"),
                id="spa",
                state=MassageListSG.state,
            ),
            Start(
                text=Const("🛻 Автопрокаты"),
                id="car_rent",
                state=CarRentSG.car_class,
            ),
            width=2,
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

        Start(
            text=Const("🙋‍♂️ Хочу в вами сотрудничать!"),
            id="cooperation",
            state=CooperationSG.input
        ),

        Start(
            Const("Админка ⚙️"),
            id="admin",
            state=AdminMainSG.state,
            when=F_User.is_superuser
        ),

        state=MainMenuSG.state
    )
)
