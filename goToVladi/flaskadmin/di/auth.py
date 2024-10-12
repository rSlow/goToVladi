from dishka import Provider, provide, Scope

from goToVladi.core.utils.auth import SecurityProps
from goToVladi.flaskadmin.utils.auth import AuthService


class AuthProvider(Provider):
    scope = Scope.APP

    @provide
    def get_auth_service(self, security: SecurityProps) -> AuthService:
        return AuthService(security)
