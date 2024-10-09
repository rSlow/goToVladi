from dishka import Provider, provide, Scope

from goToVladi.core.utils.auth import SecurityService
from goToVladi.flaskadmin.utils.auth import AuthService


class AuthProvider(Provider):
    scope = Scope.APP

    @provide
    def get_auth_service(self, security: SecurityService) -> AuthService:
        return AuthService(security)
