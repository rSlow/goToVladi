from adaptix import Retort

from goToVladi.core.config.models.paths import Paths
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config
from .admin import load_admin_config
from ..models import ApiAppConfig
from ..models.api import ApiConfig
from ..parser.auth import load_auth_config


def load_config(paths: Paths, retort: Retort) -> ApiAppConfig:
    config_dct = read_config_yaml(paths)
    api_config = retort.load(config_dct["api"], ApiConfig)
    return ApiAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        api=api_config,
        admin=load_admin_config(config_dct["api"]),
        auth=load_auth_config(config_dct["api"]["auth"])
    )
