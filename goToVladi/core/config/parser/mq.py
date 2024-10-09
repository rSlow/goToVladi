from adaptix import Retort

from ..models.mq import MQConfig


def load_mq_config(config_dct: dict, retort: Retort) -> MQConfig:
    return retort.load(config_dct, MQConfig)
