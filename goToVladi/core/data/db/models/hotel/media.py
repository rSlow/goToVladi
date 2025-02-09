from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class HotelMedia(AttachmentProtocol[dto.HotelMedia], Base):
    __tablename__ = "hotel_medias"

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    hotel = relationship("Hotel", back_populates="medias", uselist=False)
