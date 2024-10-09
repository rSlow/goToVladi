from dishka import Provider, provide, Scope, from_context
from fastapi import HTTPException, Request
from jwt import PyJWTError

from goToVladi.api.utils.auth import AuthService
from goToVladi.api.utils.auth.cookie import OAuth2PasswordBearerWithCookie
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.utils.auth import SecurityService


class AuthProvider(Provider):
    scope = Scope.APP
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide
    def get_auth_service(self, security: SecurityService) -> AuthService:
        return AuthService(security)

    @provide
    def get_cookie_auth(self) -> OAuth2PasswordBearerWithCookie:
        return OAuth2PasswordBearerWithCookie(token_url="auth/token")

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            request: Request,
            cookie_auth: OAuth2PasswordBearerWithCookie,
            auth_service: AuthService,
            dao: DaoHolder,
    ) -> dto.User:
        try:
            token = await cookie_auth.get_token(request)
            return await auth_service.get_current_user(token, dao)
        except (PyJWTError, HTTPException):
            user = await auth_service.get_user_basic(request, dao)
            if user is None:
                raise
            return user
