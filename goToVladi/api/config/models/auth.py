from dataclasses import dataclass
from datetime import timedelta
from typing import Literal


@dataclass
class AuthConfig:
    secret_key: str
    domain: str
    token_expire: timedelta
    samesite: Literal["lax", "strict", "none"] | None
    httponly: bool
    secure: bool
    auth_url: str
    algorythm: str = "HS256"
    disable_cors: bool = False
