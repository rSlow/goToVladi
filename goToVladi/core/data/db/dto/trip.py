from .attachment import BaseAttachment
from .base import BaseListCardDto, BaseCardDto
from .region import RegionMixin


class TripMedia(BaseAttachment):
    trip_id: int


class ListTrip(BaseListCardDto, RegionMixin):
    pass


class Trip(BaseCardDto, RegionMixin):
    site_url: str | None = None
    medias: list[TripMedia]
