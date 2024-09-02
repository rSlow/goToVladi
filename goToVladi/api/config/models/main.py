from __future__ import annotations

from dataclasses import dataclass



@dataclass
class ApiConfig:
    root_path: str = ""
    enable_logging: bool = False

