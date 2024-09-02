from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserDao


class DaoHolder:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

        self.user = UserDao(self.session)
