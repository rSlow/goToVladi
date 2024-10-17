from dishka import from_context, Provider, Scope, provide

from goToVladi.flaskadmin.config.models import FlaskAdminConfig, FlaskConfig
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class FlaskProvider(Provider):
    scope = Scope.APP

    config = from_context(FlaskAppConfig)

    @provide
    def get_flask_config(self, config: FlaskAppConfig) -> FlaskConfig:
        return config.flask

    @provide
    def get_admin_config(self, config: FlaskAppConfig) -> FlaskAdminConfig:
        return config.admin
