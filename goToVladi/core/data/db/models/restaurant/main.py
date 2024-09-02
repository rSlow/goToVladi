from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ..base import Base


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

    cuisine: Mapped[int] = mapped_column(
        ForeignKey('cuisines.id'), nullable=True
    )

    phones = relationship(
        "RestaurantPhone"
    )
    photos = relationship(
        "RestaurantPhoto"
    )
    socials = relationship(
        "RestaurantSocial"
    )
