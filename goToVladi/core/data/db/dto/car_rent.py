from dataclasses import dataclass, field

from .attachment import BaseAttachment
from .region import Region


@dataclass
class CarRentMedia(BaseAttachment):
    car_rent_id: int


@dataclass
class ListCarRent:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None


@dataclass
class CarClass:
    name: str

    id_: int | None = None
    description: str | None = None


@dataclass
class CarRent:
    name: str

    id_: int | None = None
    region_id: int | None = None
    region: Region | None = None
    description: str | None = None
    rating: float | None = None
    min_age: int | None = None
    min_experience: int | None = None
    min_price: int | None = None
    phone: str | None = None

    medias: list[CarRentMedia] = field(default_factory=list)
    car_classes: list[CarClass] = field(default_factory=list)
