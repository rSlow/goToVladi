from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from .app import AppConfig
from .paths import Paths
from .web import WebConfig
from ...data.db.config.models import DBConfig
from ...data.redis.config.models import RedisConfig


@dataclass
class BaseConfig(ABC):
    app: AppConfig
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    web: WebConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path

    @property
    def upload_file_path(self) -> Path:
        return self.paths.upload_file_path
