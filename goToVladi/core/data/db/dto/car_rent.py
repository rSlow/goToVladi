from .attachment import BaseAttachment
from .base import BaseListCardDto, BaseCardDto, BaseDto
from .region import RegionMixin


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
    phone: str | None = None
    medias: list[CarRentMedia]
    car_classes: list[CarClass]
