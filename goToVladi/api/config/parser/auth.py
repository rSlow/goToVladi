from typing import Any

from adaptix import Retort

from ..models.auth import AuthConfig


def load_auth_config(dct: dict[str, Any], retort: Retort) -> AuthConfig:
    return retort.load(dct, AuthConfig)
