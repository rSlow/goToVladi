from dataclasses import dataclass, field

from .attachment import BaseAttachment
from .region import Region


@dataclass
class TripMedia(BaseAttachment):
    trip_id: int


@dataclass
class ListTrip:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None


@dataclass
class Trip:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None
    description: str | None = None
    site_url: str | None = None

    medias: list[TripMedia] = field(default_factory=list)
