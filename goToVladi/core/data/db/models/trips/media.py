from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.base_attachment import BaseAttachment


class TripMedia(BaseAttachment, Base):
    __tablename__ = 'trip_medias'

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE")
    )
    trip = relationship("Trip", back_populates="medias")

    def to_dto(self) -> dto.TripMedia:
        return dto.TripMedia(
            id_=self.id,
            content=self.convert_content(),
            trip_id=self.trip_id
        )
