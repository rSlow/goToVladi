import yaml

from goToVladi.core.config.parser.paths import get_paths

bind = "0.0.0.0:5000"
wsgi_app = "goToVladi.flaskadmin.wsgi:wsgi_app"
loglevel = "info"

paths = get_paths()
with paths.logging_config_file.open("r") as f:
    logging_config = yaml.safe_load(f)

logconfig_dict = logging_config
