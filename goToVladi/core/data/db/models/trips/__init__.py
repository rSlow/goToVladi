from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin
from goToVladi.core.data.db.models.trips.media import TripMedia
from goToVladi.core.data.db.types.url import PydanticURLType


class Trip(RegionMixin, Base):
    __tablename__ = 'trips'

    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    site_url: Mapped[str | None] = mapped_column(PydanticURLType, nullable=True)
    medias: Mapped[list[TripMedia]] = relationship(cascade="all, delete-orphan")

    def to_dto(self):
        return dto.Trip(
            id_=self.id,
            name=self.name,
            description=self.description,
            site_url=self.site_url,
            medias=[_media.to_dto() for _media in self.medias],
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )

    def to_list_dto(self):
        return dto.ListTrip(
            id_=self.id,
            name=self.name,
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )

    def __str__(self):
        res = ""
        if self.region:
            res += f"{self.region.name}: "
        return res + self.name
