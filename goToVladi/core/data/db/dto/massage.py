from dataclasses import dataclass, field

from .attachment import BaseAttachment
from .region import Region


@dataclass
class MassageMedia(BaseAttachment):
    massage_id: int


@dataclass
class ListMassage:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None


@dataclass
class Massage:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None
    description: str | None = None
    min_price: float | None = None
    phone: str | None = None

    medias: list[MassageMedia] = field(default_factory=list)
