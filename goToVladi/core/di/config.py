from adaptix import Retort
from dishka import Provider, provide, Scope

from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.config.models.main import BotAppConfig
from goToVladi.bot.config.models.storage import StorageConfig
from goToVladi.bot.config.parser.main import load_config as load_bot_config
from goToVladi.core.config import Paths, BaseConfig
from goToVladi.core.config.models.web import WebConfig
from goToVladi.core.config.parser.paths import get_paths


class ConfigProvider(Provider):  # TODO все переделать
    scope = Scope.APP

    # config = from_context(BaseConfig) # TODO create pass config from context

    @provide
    def get_paths(self) -> Paths:
        return get_paths()

    @provide
    def get_bot_app_config(self, paths: Paths, retort: Retort) -> BotAppConfig:
        return load_bot_config(paths, retort)

    @provide
    def get_base_config(self, config: BotAppConfig) -> BaseConfig:
        return config

    @provide
    def get_bot_config(self, config: BotAppConfig) -> BotConfig:
        return config.bot

    @provide
    def get_bot_storage_config(self, config: BotAppConfig) -> StorageConfig:
        return config.storage

    @provide
    def get_web_config(self, config: BotAppConfig) -> WebConfig:
        return config.web
