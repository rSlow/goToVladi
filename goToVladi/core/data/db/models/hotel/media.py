from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class HotelMedia(AttachmentProtocol, Base):
    __tablename__ = "hotel_medias"

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id', ondelete="CASCADE"))
    hotel = relationship("Hotel", back_populates="medias", uselist=False)

    def to_dto(self) -> dto.HotelMedia:
        return dto.HotelMedia(
            id_=self.id,
            content=self.convert_content(),
            hotel_id=self.hotel_id
        )
