from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import AttachmentProtocol


class RestaurantMedia(AttachmentProtocol[dto.RestaurantMedia], Base):
    __tablename__ = "restaurant_medias"

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey('restaurants.id', ondelete="CASCADE"),
    )
    restaurant = relationship("Restaurant", back_populates="medias", uselist=False)
