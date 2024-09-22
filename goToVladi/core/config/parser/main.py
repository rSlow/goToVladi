from copy import copy

from adaptix import Retort

from .db import load_db_config
from .redis import load_redis_config
from .. import BaseConfig
from ..models.app import AppConfig
from ..models.paths import Paths
from ..models.static import StaticConfig, StaticType
from ..models.web import WebConfig


def load_base_config(config_dct: dict,
                     paths: Paths,
                     retort: Retort) -> BaseConfig:
    web_config = config_dct["web"]

    return BaseConfig(
        paths=paths,
        db=load_db_config(config_dct["db"], retort),
        redis=load_redis_config(config_dct["redis"], retort),
        app=load_app_config(config_dct["app"], retort),
        web=load_web_config(web_config, retort),
        static=load_static_config(config_dct["static"], web_config, retort)
    )


def load_app_config(config_dct: dict,
                    retort: Retort) -> AppConfig:
    return retort.load(config_dct, AppConfig)


def load_web_config(config_dct: dict,
                    retort: Retort) -> WebConfig:
    return retort.load(config_dct, WebConfig)


def load_static_config(
        config_dct: dict, web_config_dct: dict, retort: Retort
) -> StaticConfig:
    config_dct = copy(config_dct) | web_config_dct
    config = retort.load(config_dct, StaticConfig)
    if config.type_ == StaticType.url and not config.base_url:
        raise RuntimeError("StaticType `url` must have a base url")
    return config
