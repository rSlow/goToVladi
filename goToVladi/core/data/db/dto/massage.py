from .attachment import BaseAttachment
from .base import BaseListCardDto, BaseCardDto
from .region import RegionMixin
from ..utils.dto_types import PhoneNumberType


class MassageMedia(BaseAttachment):
    massage_id: int


class ListMassage(BaseListCardDto, RegionMixin):
    pass


class Massage(BaseCardDto, RegionMixin):
    min_price: float | None = None
    phone: PhoneNumberType | None = None
    medias: list[MassageMedia]
