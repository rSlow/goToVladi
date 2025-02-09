from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class TripMedia(AttachmentProtocol[dto.TripMedia], Base):
    __tablename__ = "trip_medias"

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE")
    )
    trip = relationship("Trip", back_populates="medias")
