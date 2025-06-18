from operator import attrgetter

from .attachment import BaseAttachment, FileSchema
from .car_rent import CarRent, CarRentMedia, CarClass, ListCarRent
from .cooperation import Cooperation
from .food import FoodCuisine
from .food.bar import Bar, BarMedia, ListBar
from .food.breakfast import Breakfast, BreakfastMedia, ListBreakfast
from .food.delivery import Delivery, DeliveryMedia, ListDelivery
from .food.restaurant import Restaurant, RestaurantMedia, ListRestaurant
from .hotel import Hotel, ListHotel, HotelMedia, HotelDistrict
from .log_event import LogEvent
from .massage import Massage, ListMassage, MassageMedia
from .message_text import MessageText
from .region import Region
from .sea_recreation import SeaRecreation, ListSeaRecreation, SeaRecreationMedia, \
    SeaRecreationCategory
from .settings import Setting
from .trip import Trip, ListTrip, TripMedia
from .user import User, UserWithCreds, UserRole

id_getter = attrgetter("id")
