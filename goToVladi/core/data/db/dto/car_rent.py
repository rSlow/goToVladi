from .attachment import BaseAttachment
from .base import BaseListCardDto, BaseCardDto, BaseDto
from .region import RegionMixin
from ..utils.dto_types import PhoneNumberType


class CarRentMedia(BaseAttachment):
    car_rent_id: int


class ListCarRent(BaseListCardDto, RegionMixin):
    pass


class CarClass(BaseDto):
    name: str
    description: str | None = None


class CarRent(BaseCardDto, RegionMixin):
    rating: float | None = None
    min_age: int | None = None
    min_experience: int | None = None
    min_price: int | None = None
    phone: PhoneNumberType | None = None
    site_url: str | None = None
    medias: list[CarRentMedia]
    car_classes: list[CarClass]
