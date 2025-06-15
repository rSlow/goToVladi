from dataclasses import dataclass


@dataclass
class AppConfig:
    name: str
    version: str | int
    admins: list[int]
