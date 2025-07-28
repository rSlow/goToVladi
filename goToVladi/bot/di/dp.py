import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage, \
    DefaultKeyBuilder
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.manager.bg_manager import BgManagerFactoryImpl
from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from goToVladi.bot.config.models.storage import StorageConfig, StorageType
from goToVladi.core.factory.redis import create_redis

logger = logging.getLogger(__name__)


class DpProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
            self,
            event_isolation: BaseEventIsolation,
            storage: BaseStorage,
    ) -> Dispatcher:
        return Dispatcher(storage=storage, events_isolation=event_isolation)

    @provide
    def create_storage(self, config: StorageConfig) -> BaseStorage:
        logger.info("creating storage for type %s", config.type_)
        match config.type_:
            case StorageType.memory:
                storage = MemoryStorage()
            case StorageType.redis:
                if config.redis is None:
                    raise ValueError(
                        "you have to specify redis config for use redis storage"
                    )
                storage = RedisStorage(
                    redis=create_redis(config.redis),
                    key_builder=DefaultKeyBuilder(with_destiny=True)
                )
            case _:
                raise NotImplementedError

        return storage

    @provide
    def get_event_isolation(self, redis: Redis) -> BaseEventIsolation:
        return RedisEventIsolation(redis)

    @provide
    def get_bg_manager_factory(self, dp: Dispatcher) -> BgManagerFactory:
        return BgManagerFactoryImpl(dp)


def resolve_update_types(dp: Dispatcher) -> list[str]:
    return dp.resolve_used_update_types(skip_events={"aiogd_update"})
