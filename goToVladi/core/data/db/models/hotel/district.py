from sqlalchemy.orm import Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class HotelDistrict(Base):
    __tablename__ = 'hotel_districts'

    name: Mapped[str]

    def to_dto(self):
        return dto.HotelDistrict(

        )