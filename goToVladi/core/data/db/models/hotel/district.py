from sqlalchemy.orm import Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base, mixins


class HotelDistrict(mixins.RegionMixin, Base):
    __tablename__ = 'hotel_districts'

    name: Mapped[str]
    hotels = relationship("Hotel", back_populates="district", uselist=True)

    def to_dto(self):
        return dto.HotelDistrict.model_validate(self)

    def __str__(self):
        res = ""
        if self.region:
            res += f"{self.region.name}: "
        return res + self.name
