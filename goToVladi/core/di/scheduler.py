from typing import AsyncIterable

from dishka import Provider, Scope, provide, AsyncContainer

from goToVladi.core.data.redis.config.models import RedisConfig
from goToVladi.core.scheduler.scheduler import Scheduler, ApScheduler


class SchedulerProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_scheduler(
            self, dishka: AsyncContainer, redis_config: RedisConfig
    ) -> AsyncIterable[Scheduler]:
        async with ApScheduler(
                dishka=dishka,
                redis_config=redis_config
        ) as scheduler:
            yield scheduler
