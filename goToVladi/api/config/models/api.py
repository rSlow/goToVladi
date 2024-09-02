from __future__ import annotations

from dataclasses import dataclass

from goToVladi.core.config import BaseConfig
from .main import ApiConfig


@dataclass
class ApiAppConfig(BaseConfig):
    api: ApiConfig

    @classmethod
    def from_base(cls,
                  base: BaseConfig,
                  api: ApiConfig):
        return cls(
            paths=base.paths,
            db=base.db,
            redis=base.redis,
            api=api,
            app=base.app,
            web=base.web,
        )
