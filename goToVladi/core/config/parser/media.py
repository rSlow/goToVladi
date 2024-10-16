from copy import copy

from adaptix import Retort

from ..models.media import MediaConfig, MediaLoadType


def load_media_config(
        config_dct: dict, web_config_dct: dict, retort: Retort
) -> MediaConfig:
    config_dct = copy(config_dct) | web_config_dct
    media_config = retort.load(config_dct, MediaConfig)
    if media_config.type_ == MediaLoadType.url and not media_config.base_url:
        raise RuntimeError("MediaLoadType `url` must have a `path` for mount")
    return media_config
