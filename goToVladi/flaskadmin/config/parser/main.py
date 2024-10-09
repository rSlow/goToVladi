from adaptix import Retort

from goToVladi.core.config import Paths
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config
from goToVladi.flaskadmin.config.models.main import FlaskConfig, FlaskAppConfig
from goToVladi.flaskadmin.config.parser.admin import load_admin_config


def load_config(paths: Paths, retort: Retort):
    data = read_config_yaml(paths)
    flask_config = data["flask"]
    return FlaskAppConfig.from_base(
        base=load_base_config(data, paths, retort),
        flask=retort.load(flask_config, FlaskConfig),
        admin=load_admin_config(flask_config["admin"], retort)
    )
