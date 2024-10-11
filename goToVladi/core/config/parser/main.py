from adaptix import Retort

from .auth import load_auth_config
from .db import load_db_config
from .mq import load_mq_config
from .redis import load_redis_config
from .static import load_static_config
from .. import BaseConfig
from ..models.app import AppConfig
from ..models.paths import Paths
from ..models.web import WebConfig


def load_base_config(
        config_dct: dict, paths: Paths, retort: Retort
) -> BaseConfig:
    web_config = config_dct["web"]

    return BaseConfig(
        paths=paths,
        db=load_db_config(config_dct["db"], retort),
        redis=load_redis_config(config_dct["redis"], retort),
        app=retort.load(config_dct["app"], AppConfig),
        web=retort.load(config_dct["web"], WebConfig),
        media=load_static_config(config_dct["media"], web_config, retort),
        mq=load_mq_config(config_dct["mq"], retort),
        auth=load_auth_config(
            config_dct["auth"],
            base_url=config_dct["web"]["base-url"],
            bot_token=config_dct["bot"]["token"],
            retort=retort
        )
    )
