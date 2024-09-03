from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db.models import Base


class RestaurantType(Enum):
    DELIVERY = "DELIVERY"
    INNER = "INNER"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    average_check: Mapped[int]
    site_url: Mapped[str] = mapped_column(nullable=True)
    type_ = mapped_column(
        PgEnum(RestaurantType, name="restaurant_type")
    )
    rating: Mapped[float]
    priority: Mapped[float] = mapped_column(default=0)

    cuisine_id: Mapped[int] = mapped_column(
        ForeignKey('restaurant_cuisines.id'), nullable=True
    )

    cuisine = relationship("RestaurantCuisine", foreign_keys=cuisine_id)
    phones = relationship(
        "RestaurantPhone",
        back_populates="restaurant",
        foreign_keys="RestaurantPhone.restaurant_id",
    )
    photos = relationship(
        "RestaurantPhoto",
        back_populates="restaurant",
        foreign_keys="RestaurantPhoto.restaurant_id",
    )
    socials = relationship(
        "RestaurantSocial",
        back_populates="restaurant",
        foreign_keys="RestaurantSocial.restaurant_id",
    )
