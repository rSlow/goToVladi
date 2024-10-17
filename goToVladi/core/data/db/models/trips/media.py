from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import FileField
from sqlalchemy_file.validators import SizeValidator

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class TripMedia(AttachmentProtocol, Base):
    __tablename__ = 'trip_medias'

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE")
    )
    trip = relationship("Trip", back_populates="medias")
    content = mapped_column(
        FileField(
            upload_storage="trips",
            validators=[SizeValidator(max_size="50M")]
        )
    )

    def to_dto(self) -> dto.TripMedia:
        return dto.TripMedia(
            id_=self.id,
            content=self.convert_content(),
            trip_id=self.trip_id
        )
