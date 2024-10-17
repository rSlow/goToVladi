from dataclasses import dataclass


@dataclass
class MediaConfig:
    path: str
    base_url: str = "/media"
