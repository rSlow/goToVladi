from dishka import Provider, Scope, from_context, provide

from goToVladi.core.config.models.db import DBConfig
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(FlaskAppConfig)

    @provide
    def db_config(self, flask_config: FlaskAppConfig) -> DBConfig:
        return flask_config.db
