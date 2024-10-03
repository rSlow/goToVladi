from dishka import Provider, Scope, from_context

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(FlaskAppConfig)
