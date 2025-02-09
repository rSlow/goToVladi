from goToVladi.core.data.db.dto.base import BaseDto


class Region(BaseDto):
    name: str


class RegionMixin:
    region: Region | None = None
    region_id: int | None = None
