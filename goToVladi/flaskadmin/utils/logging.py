from logging.config import dictConfig

import yaml

from goToVladi.core.config.parser.paths import get_paths


def setup_logging():
    paths = get_paths()
    with paths.logging_config_file.open("r") as f:
        logging_config = yaml.safe_load(f)

    dictConfig(logging_config)
