from dataclasses import dataclass, field

from goToVladi.core.data.db.dto import BaseAttachment
from .region import Region


@dataclass
class HotelMedia(BaseAttachment):
    hotel_id: int


@dataclass
class HotelDistrict:
    name: str
    region_id: int | None = None
    region: Region | None = None


@dataclass
class ListHotel:
    name: str
    district: HotelDistrict
    min_price: int

    id_: int | None = None


@dataclass
class Hotel:
    name: str
    min_price: int

    medias: list[HotelMedia] = field(default_factory=list)

    district: HotelDistrict | None = None
    district_id: int | None = None
    id_: int | None = None
    promo_code: str | None = None
    site_url: str | None = None
    description: str | None = None
