from goToVladi.core.data.db.dto import BaseAttachment
from goToVladi.core.data.db.dto.base import BaseCardDto, BaseListCardDto
from goToVladi.core.data.db.dto.region import RegionMixin
from goToVladi.core.data.db.utils.dto_types import PhoneNumberType


class BarMedia(BaseAttachment):
    bar_id: int


class ListBar(BaseListCardDto, RegionMixin):
    rating: float | None = None
    average_check: int | None = None


class Bar(BaseCardDto, RegionMixin):
    average_check: int | None = None
    rating: float
    phone: PhoneNumberType | None = None
    medias: list[BarMedia]
