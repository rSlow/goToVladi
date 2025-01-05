from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class CarRentMedia(AttachmentProtocol, Base):
    __tablename__ = "car_rent_medias"

    car_rent_id: Mapped[int] = mapped_column(ForeignKey('car_rents.id', ondelete="CASCADE"))
    car_rent = relationship("CarRent", back_populates="medias", uselist=False)

    def to_dto(self) -> dto.CarRentMedia:
        return dto.CarRentMedia(
            id_=self.id,
            content=self.convert_content(),
            car_rent_id=self.car_rent_id
        )
