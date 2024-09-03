from datetime import timedelta
from typing import Any

from ..models.auth import AuthConfig


def load_auth_config(dct: dict[str, Any]) -> AuthConfig:
    return AuthConfig(
        token_expire=timedelta(seconds=dct["token-expire"]),
        domain=dct["domain"],
        secret_key=dct["secret-key"],
        samesite=dct["samesite"],
        httponly=bool(dct["httponly"]),
        secure=bool(dct["secure"]),
        auth_url=dct["auth-url"],
        algorythm=dct["algorythm"],
        disable_cors=bool(dct.get("disable-cors", False))
    )
