from dishka import Provider, Scope, provide

from goToVladi.core.config.models import SecurityConfig
from goToVladi.core.utils.auth.security import SecurityService


class SecurityProvider(Provider):
    scope = Scope.APP

    @provide
    def get_auth_service(self, config: SecurityConfig) -> SecurityService:
        return SecurityService(config)
