from .config import ConfigProvider
from .db import DbProvider
from .lock import LockProvider
from .redis import RedisProvider
from .retort import RetortProvider
from .scheduler import SchedulerProvider


def get_common_providers():
    return [
        ConfigProvider(),
        RetortProvider(),
        DbProvider(),
        RedisProvider(),
        LockProvider(),
        SchedulerProvider()
    ]
