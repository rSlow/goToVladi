from adaptix import Retort
from dishka import Provider, Scope, provide

from goToVladi.api.config.models import ApiAppConfig
from goToVladi.api.config.models.api import ApiConfig
from goToVladi.api.config.parser.main import load_config
from goToVladi.core.config import Paths


class ApiConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_api_app_config(
            self, paths: Paths, base_retort: Retort
    ) -> ApiAppConfig:
        return load_config(paths, base_retort)

    @provide
    def get_api_config(self, api_app: ApiAppConfig) -> ApiConfig:
        return api_app.api
