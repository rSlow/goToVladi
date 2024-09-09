from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    app_dir: Path

    @property
    def config_path(self) -> Path:
        return self.app_dir / "config"

    @property
    def config_file(self) -> Path:
        return self.config_path / "config.yml"

    @property
    def logging_config_file(self) -> Path:
        return self.config_path / "logging.yml"

    @property
    def log_path(self) -> Path:
        return self.app_dir / "log"

    @property
    def version_path(self) -> Path:  # TODO check
        return self.app_dir / "version.yaml"

    @property
    def src_path(self) -> Path:
        return self.app_dir / "goToVladi"

    @property
    def upload_file_path(self) -> Path:
        return self.src_path / "core" / "data" / "db" / "upload"
