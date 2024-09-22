from typing import Any

from adaptix import Retort

from ..models.auth import AuthConfig


def load_auth_config(
        config_dct: dict[str, Any], base_url: str, retort: Retort
) -> AuthConfig:
    config_dct["domain"] = base_url
    return retort.load(config_dct, AuthConfig)
