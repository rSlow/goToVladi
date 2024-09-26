from dataclasses import dataclass, field

from goToVladi.core.data.db.dto import BaseAttachment


@dataclass
class HotelMedia(BaseAttachment):
    hotel_id: int


@dataclass
class ListHotel:
    name: str
    district: str
    min_price: int

    id_: int | None = None


@dataclass
class Hotel:
    name: str
    district: str
    min_price: int

    medias: list[HotelMedia] = field(default_factory=list)

    id_: int | None = None
    promo_code: str | None = None
    site_url: str | None = None
    description: str | None = None
