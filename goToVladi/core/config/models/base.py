from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .db import DBConfig
from .redis import RedisConfig
from .app import AppConfig
from .paths import Paths
from .static import StaticConfig
from .web import WebConfig


@dataclass
class BaseConfig:
    app: AppConfig
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    web: WebConfig
    static: StaticConfig

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
