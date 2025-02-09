from goToVladi.core.data.db.dto import BaseAttachment
from .base import BaseDto, BaseListCardDto, BaseCardDto
from .region import RegionMixin


class HotelMedia(BaseAttachment):
    hotel_id: int


class HotelDistrict(BaseDto, RegionMixin):
    name: str


class ListHotel(BaseListCardDto):
    district: HotelDistrict
    min_price: int


class Hotel(BaseCardDto):
    min_price: int
    medias: list[HotelMedia]
    district: HotelDistrict | None = None
    district_id: int | None = None
    promo_code: str | None = None
    site_url: str | None = None
