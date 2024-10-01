from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.base_attachment import BaseAttachment


class RestaurantMedia(BaseAttachment, Base):
    __tablename__ = 'restaurant_medias'

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey('restaurants.id'), ondelete="CASCADE"
    )

    def to_dto(self) -> dto.RestaurantMedia:
        return dto.RestaurantMedia(
            id_=self.id,
            content_type=self.content_type,
            content=self.convert_content(),
            restaurant_id=self.restaurant_id
        )
