from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
from urllib.parse import urlparse


@dataclass
class SecurityConfig:
    secret_key: str
    domain: str
    tg_bot_username: str
    token_expire: timedelta
    samesite: Literal["lax", "strict", "none"] | None
    httponly: bool
    secure: bool
    algorythm: str = "HS256"
    disable_cors: bool = False

    @property
    def host(self):
        url = urlparse(self.domain)
        return url.netloc
