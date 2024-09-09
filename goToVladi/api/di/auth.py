from dishka import Provider, provide, Scope, from_context
from fastapi import HTTPException, Request
from jwt import PyJWTError

from goToVladi.api.config.models.auth import AuthConfig
from goToVladi.api.utils.auth import AuthService
from goToVladi.api.utils.auth.cookie import OAuth2PasswordBearerWithCookie
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder


class AuthProvider(Provider):
    scope = Scope.APP
    request = from_context(provides=Request)

    @provide
    def get_auth_service(self, config: AuthConfig) -> AuthService:
        return AuthService(config)

    @provide
    def get_cookie_auth(self) -> OAuth2PasswordBearerWithCookie:
        return OAuth2PasswordBearerWithCookie(
            token_url="auth/token"
        )  # TODO set token url

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            request: Request,
            cookie_auth: OAuth2PasswordBearerWithCookie,
            auth_service: AuthService,
            dao: DaoHolder,
    ) -> dto.User:
        try:
            token = cookie_auth.get_token(request)
            return await auth_service.get_current_user(token, dao)
        except (PyJWTError, HTTPException):
            user = await auth_service.get_user_basic(request, dao)
            if user is None:
                raise
            return user
