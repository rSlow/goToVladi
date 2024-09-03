from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db.models import Base


class RestaurantPhoto(Base):
    __tablename__ = 'restaurant_photos'

    id: Mapped[int] = mapped_column(primary_key=True)
    url = mapped_column(URLType)

    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    restaurant = relationship(
        "Restaurant",
        foreign_keys=restaurant_id,
        back_populates="photos",
    )
