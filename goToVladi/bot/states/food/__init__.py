from goToVladi.bot.utils.states_factory import FSMSingleFactory
from .bar import BarCardSG, BarListSG
from .delivery import DeliveryCardSG, DeliveryListSG
from .restaurant import RestaurantCardSG, RestaurantListSG
from .breakfast import BreakfastCardSG, BreakfastListSG

FoodCategorisesSG = FSMSingleFactory("FoodCategorisesSG")
