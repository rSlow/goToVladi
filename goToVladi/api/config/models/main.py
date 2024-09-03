from __future__ import annotations

from dataclasses import dataclass

from goToVladi.api.config.models.admin import AdminConfig
from goToVladi.core.config import BaseConfig
from .api import ApiConfig
from .auth import AuthConfig


@dataclass
class ApiAppConfig(BaseConfig):
    api: ApiConfig
    admin: AdminConfig
    auth: AuthConfig

    @classmethod
    def from_base(cls,
                  base: BaseConfig,
                  api: ApiConfig,
                  admin: AdminConfig,
                  auth: AuthConfig):
        return cls(
            paths=base.paths,
            db=base.db,
            redis=base.redis,
            api=api,
            app=base.app,
            web=base.web,
            admin=admin,
            auth=auth
        )