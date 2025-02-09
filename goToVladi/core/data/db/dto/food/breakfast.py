from goToVladi.core.data.db.dto import BaseAttachment
from goToVladi.core.data.db.dto.base import BaseCardDto, BaseListCardDto
from goToVladi.core.data.db.dto.region import RegionMixin
from goToVladi.core.data.db.utils.dto_types import PhoneNumberType


class BreakfastMedia(BaseAttachment):
    breakfast_id: int


class ListBreakfast(BaseListCardDto, RegionMixin):
    rating: float | None = None
    average_check: int | None = None


class Breakfast(BaseCardDto, RegionMixin):
    average_check: int | None = None
    rating: float
    phone: PhoneNumberType | None = None
    medias: list[BreakfastMedia]
