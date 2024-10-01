from sqlalchemy.orm import Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base, mixins


class HotelDistrict(mixins.RegionMixin, Base):
    __tablename__ = 'hotel_districts'

    name: Mapped[str]

    def to_dto(self):
        return dto.HotelDistrict(
            name=self.name,
            region_id=self.region_id,
            region=self.region.to_dto() if self.region else None,
        )
