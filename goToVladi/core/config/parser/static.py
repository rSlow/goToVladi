from copy import copy

from adaptix import Retort

from ..models.static import StaticConfig, StaticType


def load_static_config(
        config_dct: dict, web_config_dct: dict, retort: Retort
) -> StaticConfig:
    config_dct = copy(config_dct) | web_config_dct
    config = retort.load(config_dct, StaticConfig)
    if config.type_ == StaticType.url and not config.base_url:
        raise RuntimeError("StaticType `url` must have a base url")
    return config
