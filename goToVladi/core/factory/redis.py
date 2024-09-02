import logging

from redis.asyncio import Redis
from goToVladi.core.data.redis.config.models import RedisConfig

logger = logging.getLogger(__name__)


def create_redis(config: RedisConfig) -> Redis:
    logger.info("created redis for %s", config)
    return Redis(
        host=config.host,
        port=config.port,
        db=config.db,
        password=config.password
    )
