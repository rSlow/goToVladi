from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, \
    OAuthFlowPassword
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.responses import Response

from goToVladi.api.config.models.auth import AuthConfig
from goToVladi.api.config.models.token import Token


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            auto_error: bool = True
    ):
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=token_url))
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error
        )

    @staticmethod
    async def get_token(request: Request) -> Token:
        authorization = request.cookies.get("Authorization", "")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return Token(token=param, token_type="bearer")

    __call__ = get_token


def set_auth_cookie(config: AuthConfig, response: Response, token: Token):
    response.set_cookie(
        "Authorization",
        value=f"{token.token_type} {token.token}",
        samesite=config.samesite,
        domain=config.domain,
        httponly=config.httponly,
        secure=config.secure,
        max_age=config.token_expire.seconds,
    )
