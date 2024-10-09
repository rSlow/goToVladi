from dishka import from_context, Provider, Scope

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class FlaskProvider(Provider):
    scope = Scope.APP

    config = from_context(FlaskAppConfig)
