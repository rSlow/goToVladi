from dataclasses import dataclass
from enum import Enum


class StaticType(Enum):
    url = "url"
    path = "path"


@dataclass
class StaticConfig:
    type_: StaticType
    base_url: str | None = None
