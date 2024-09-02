from adaptix import Retort

from .. import BaseConfig
from ..models.app import AppConfig
from ..models.paths import Paths
from ..models.web import WebConfig
from ...data.db.config.parser.main import load_db_config
from ...data.redis.config.parser.main import load_redis_config


def load_base_config(config_dct: dict,
                     paths: Paths,
                     retort: Retort) -> BaseConfig:
    return BaseConfig(
        paths=paths,
        db=load_db_config(config_dct["db"], retort),
        redis=load_redis_config(config_dct["redis"], retort),
        app=load_app_config(config_dct["app"], retort),
        web=load_web_config(config_dct["web"], retort),
    )


def load_app_config(config_dct: dict,
                    retort: Retort) -> AppConfig:
    return retort.load(config_dct, AppConfig)


def load_web_config(config_dct: dict,
                    retort: Retort) -> WebConfig:
    return retort.load(config_dct, WebConfig)
