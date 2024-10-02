from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from goToVladi.core.config.models import BaseConfig
from goToVladi.core.config.models.db import DBConfig
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.factory.db.a_sync import create_engine, create_session_maker


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, base_config: BaseConfig) -> DBConfig:
        return base_config.db

    @provide
    async def get_engine(
            self, db_config: DBConfig
    ) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(db_config)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_dao(self, session: AsyncSession, redis: Redis) -> DaoHolder:
        return DaoHolder(session=session, redis=redis)
