from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .hotel import HotelDao
from .restaurant import RestaurantDao
from .user import UserDao


class DaoHolder:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

        self.user: UserDao = UserDao(self.session)
        self.restaurant: RestaurantDao = RestaurantDao(self.session)
        self.hotel: HotelDao = HotelDao(self.session)
