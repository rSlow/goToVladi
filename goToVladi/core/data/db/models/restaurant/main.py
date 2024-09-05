from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dto.restaurant import RestaurantType
from goToVladi.core.data.db.models import Base
from .cuisine import RestaurantCuisine
from .phone import RestaurantPhone
from .photo import RestaurantPhoto
from .social import RestaurantSocial


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    average_check: Mapped[int]
    description = mapped_column(Text(), nullable=True)
    site_url: Mapped[str] = mapped_column(nullable=True)
    type_ = mapped_column(
        PG_ENUM(RestaurantType, name="restaurant_type")
    )
    rating: Mapped[float]
    priority: Mapped[float] = mapped_column(default=0)

    cuisine_id: Mapped[int] = mapped_column(
        ForeignKey('restaurant_cuisines.id'), nullable=True
    )

    cuisine: Mapped[RestaurantCuisine] = relationship(
        "RestaurantCuisine",
        foreign_keys=cuisine_id
    )

    phones: Mapped[list[RestaurantPhone]] = relationship(
        "RestaurantPhone",
        back_populates="restaurant",
        foreign_keys="RestaurantPhone.restaurant_id",
    )
    photos: Mapped[list[RestaurantPhoto]] = relationship(
        "RestaurantPhoto",
        back_populates="restaurant",
        foreign_keys="RestaurantPhoto.restaurant_id",
    )
    socials: Mapped[list[RestaurantSocial]] = relationship(
        "RestaurantSocial",
        back_populates="restaurant",
        foreign_keys="RestaurantSocial.restaurant_id",
    )

    def to_dto(self) -> dto.Restaurant:
        return dto.Restaurant(
            id_=self.id,
            name=self.name,
            average_check=self.average_check,
            type_=self.type_,
            rating=self.rating,
            priority=self.priority,
            site_url=self.site_url,
            description=self.description,
            cuisine=self.cuisine.to_dto(),
            phones=[phone.to_dto() for phone in self.phones],
            photos=[photo.to_dto() for photo in self.photos],
            socials=[social.to_dto() for social in self.socials],
        )
