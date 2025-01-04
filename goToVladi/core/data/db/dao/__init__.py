from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .hotel import HotelDao
from .log import EventLogDao
from .massage import MassageDao
from .region import RegionDao
from .restaurant import RestaurantDao
from .trip import TripDao
from .user import UserDao


class DaoHolder:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

        self.user: UserDao = UserDao(self.session)
        self.region: RegionDao = RegionDao(self.session)
        self.log: EventLogDao = EventLogDao(self.session)

        self.restaurant: RestaurantDao = RestaurantDao(self.session)
        self.hotel: HotelDao = HotelDao(self.session)
        self.trip: TripDao = TripDao(self.session)
        self.massage: MassageDao = MassageDao(self.session)
