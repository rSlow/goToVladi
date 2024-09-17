from operator import attrgetter

from .restaurant import Restaurant, RestaurantCuisine
from .user import User, UserWithCreds

id_getter = attrgetter("id_")
