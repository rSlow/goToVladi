from dataclasses import dataclass
from enum import Enum


class MediaLoadType(Enum):
    url = "url"
    path = "path"


@dataclass
class MediaConfig:
    type_: MediaLoadType
    base_url: str | None = None
    path: str | None = None
