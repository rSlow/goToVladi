import logging
from asyncio import Protocol

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from redis import Redis

from goToVladi.core.config.models.redis import RedisConfig
from goToVladi.core.scheduler.context import SchedulerInjectContext

logger = logging.getLogger(__name__)


class Scheduler(Protocol):
    async def start(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def __aenter__(self):
        logger.info("Starting scheduler")
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class ApScheduler(Scheduler):
    def __init__(self, dishka: AsyncContainer, redis_config: RedisConfig):
        SchedulerInjectContext.container = dishka
        self.job_store = RedisJobStore(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password
        )
        self.job_store.redis = Redis.from_url(redis_config.uri)
        self.executor = AsyncIOExecutor()
        job_defaults = {  # TODO check
            "coalesce": False,
            "max_instances": 20,
            "misfire_grace_time": 3600,
        }
        logger.info("configuring shedulder...")
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": self.job_store},
            job_defaults=job_defaults,
            executors={"default": self.executor},
        )

    async def start(self):
        self.scheduler.start()

    async def close(self):
        self.scheduler.shutdown()
        self.executor.shutdown()
        self.job_store.shutdown()
