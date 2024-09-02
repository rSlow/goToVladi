from typing import Any

from adaptix import Retort

from goToVladi.core.data.redis.config.parser.main import load_redis_config
from ..models.storage import StorageConfig, StorageType


def load_storage_config(dct: dict[str, Any],
                        retort: Retort) -> StorageConfig:
    config = StorageConfig(type_=StorageType[dct["type"]])
    if config.type_ == StorageType.redis:
        config.redis = load_redis_config(dct["redis"], retort)
    return config
