from adaptix import Retort

from goToVladi.api.config.models.api import ApiAppConfig
from goToVladi.api.config.models.main import ApiConfig
from goToVladi.core.config.models.paths import Paths
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config


def load_config(paths: Paths,
                retort: Retort) -> ApiAppConfig:
    config_dct = read_config_yaml(paths)
    api_config = retort.load(config_dct["api"], ApiConfig)
    return ApiAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        api=api_config
    )
