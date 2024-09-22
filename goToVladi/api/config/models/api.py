from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApiConfig:
    enable_logging: bool = False
