from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class CarRentMedia(AttachmentProtocol[dto.CarRentMedia], Base):
    __tablename__ = "car_rent_medias"

    car_rent_id: Mapped[int] = mapped_column(ForeignKey('car_rents.id', ondelete="CASCADE"))
    car_rent = relationship("CarRent", back_populates="medias", uselist=False)
