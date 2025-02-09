from goToVladi.core.data.db.dto import BaseAttachment
from goToVladi.core.data.db.dto.base import BaseDto, BaseListCardDto, BaseCardDto
from goToVladi.core.data.db.dto.region import RegionMixin
from goToVladi.core.data.db.utils.dto_types import PhoneNumberType


class SeaRecreationMedia(BaseAttachment):
    sea_recreation_id: int


class SeaRecreationCategory(BaseDto):
    name: str


class ListSeaRecreation(BaseListCardDto, RegionMixin):
    category: SeaRecreationCategory | None = None


class SeaRecreation(BaseCardDto, RegionMixin):
    phone: PhoneNumberType | None = None
    rating: float | None = None
    category: SeaRecreationCategory | None = None
    medias: list[SeaRecreationMedia]
