from .config import BaseConfigProvider
from .db import DbProvider
from .lock import LockProvider
from .redis import RedisProvider
from .retort import RetortProvider
from .scheduler import SchedulerProvider


def get_common_providers():
    return [
        BaseConfigProvider(),
        RetortProvider(),
        DbProvider(),
        RedisProvider(),
        LockProvider(),
        SchedulerProvider()
    ]
