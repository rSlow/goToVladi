from dishka import Provider, provide, Scope, from_context

from goToVladi.core.config.models import (
    Paths, BaseConfig, WebConfig, MQConfig, SecurityConfig, AppConfig,
    StaticConfig
)


class BaseConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(BaseConfig)

    @provide
    def get_paths(self, config: BaseConfig) -> Paths:
        return config.paths

    @provide
    def get_web_config(self, config: BaseConfig) -> WebConfig:
        return config.web

    @provide
    def get_mq_config(self, config: BaseConfig) -> MQConfig:
        return config.mq

    @provide
    def get_auth_config(self, config: BaseConfig) -> SecurityConfig:
        return config.auth

    @provide
    def get_app_config(self, config: BaseConfig) -> AppConfig:
        return config.app

    @provide
    def get_static_config(self, config: BaseConfig) -> StaticConfig:
        return config.static
