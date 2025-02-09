from .attachment import BaseAttachment
from .base import BaseListCardDto, BaseCardDto
from .region import RegionMixin


class MassageMedia(BaseAttachment):
    massage_id: int


class ListMassage(BaseListCardDto, RegionMixin):
    pass


class Massage(BaseCardDto, RegionMixin):
    min_price: float | None = None
    phone: str | None = None
    medias: list[MassageMedia]
