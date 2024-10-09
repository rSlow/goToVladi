from adaptix import Retort

from goToVladi.core.config import Paths
from goToVladi.core.config.parser.main import load_base_config
from goToVladi.mq.config.models.main import MQAppConfig


def load_config(data: dict, paths: Paths, retort: Retort):
    return MQAppConfig.from_base(
        base=load_base_config(data, paths, retort),
    )
