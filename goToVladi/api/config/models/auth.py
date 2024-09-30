from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
from urllib.parse import urlparse


@dataclass
class AuthConfig:
    secret_key: str
    domain: str
    bot_username: str
    token_expire: timedelta
    samesite: Literal["lax", "strict", "none"] | None
    httponly: bool
    secure: bool
    auth_path: str
    algorythm: str = "HS256"
    disable_cors: bool = False

    @property
    def host(self):
        url = urlparse(self.domain)
        return url.netloc
