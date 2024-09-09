import logging

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

from goToVladi.core.data.db.config.models import DBConfig

logger = logging.getLogger(__name__)


def create_pool(db_config: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(db_config)
    return create_session_maker(engine)


def create_engine(db_config: DBConfig) -> AsyncEngine:
    logger.info("created db engine for %s", db_config)
    logger.debug(db_config.uri)
    return create_async_engine(
        url=make_url(db_config.uri),
        echo=db_config.echo
    )


def create_session_maker(
        engine: AsyncEngine
) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
    return pool
