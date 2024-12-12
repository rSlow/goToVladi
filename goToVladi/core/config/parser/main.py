from adaptix import Retort

from .auth import load_auth_config
from .redis import load_redis_config
from .. import BaseConfig
from ..models import MediaConfig, DBConfig, MQConfig
from ..models.app import AppConfig
from ..models.paths import Paths
from ..models.web import WebConfig


def load_base_config(
        config_dct: dict, paths: Paths, retort: Retort
) -> BaseConfig:
    web_config = config_dct["web"]

    return BaseConfig(
        paths=paths,
        db=retort.load(config_dct["db"], DBConfig),
        redis=load_redis_config(config_dct["redis"], retort),
        app=retort.load(config_dct["app"], AppConfig),
        web=retort.load(web_config, WebConfig),
        media=retort.load(config_dct["media"], MediaConfig),
        mq=retort.load(config_dct["mq"], MQConfig),
        auth=load_auth_config(
            config_dct["auth"],
            base_url=web_config["base-url"],
            bot_token=config_dct["bot"]["token"],
            retort=retort
        )
    )
