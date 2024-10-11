from adaptix import Retort

from goToVladi.bot.config.models.main import BotAppConfig
from goToVladi.bot.config.parser.bot import load_bot_config
from goToVladi.bot.config.parser.storage import load_storage_config
from goToVladi.core.config.models.paths import Paths
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config


def load_config(paths: Paths, retort: Retort) -> BotAppConfig:
    config_dct = read_config_yaml(paths)

    return BotAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        bot=load_bot_config(
            config_dct["bot"],
            config_dct["web"]["base-url"],
            retort
        ),
        storage=load_storage_config(config_dct, retort),
    )
