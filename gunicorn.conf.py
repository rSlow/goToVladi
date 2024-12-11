import yaml

from goToVladi.core.config.parser.paths import get_paths

bind = "0.0.0.0:5000"
wsgi_app = "goToVladi.flaskadmin.__main__:main()"
loglevel = "info"
workers = 1

paths = get_paths()
with paths.logging_config_file.open("r") as f:
    logging_config = yaml.safe_load(f)

logconfig_dict = logging_config
