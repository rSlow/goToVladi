from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.base_attachment import BaseAttachment


class HotelMedia(BaseAttachment, Base):
    __tablename__ = 'hotel_medias'

    hotel_id: Mapped[int] = mapped_column(
        ForeignKey('hotels.id', ondelete="CASCADE")
    )

    def to_dto(self) -> dto.HotelMedia:
        return dto.HotelMedia(
            id_=self.id,
            content_type=self.content_type,
            content=self.convert_content(),
            hotel_id=self.hotel_id
        )
