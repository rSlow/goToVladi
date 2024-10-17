from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApiConfig:
    root_path: str = ""
    enable_logging: bool = False
    debug: bool = False

    def get_real_root_path(self, base_root_path: str | None) -> str | None:
        if self.root_path or base_root_path:
            return (base_root_path or "") + self.root_path
