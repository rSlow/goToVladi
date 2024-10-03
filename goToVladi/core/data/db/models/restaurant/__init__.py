from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType, PhoneNumberType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins import RegionMixin
from goToVladi.core.data.db.models.restaurant.cuisine import RestaurantCuisine
from goToVladi.core.data.db.models.restaurant.media import RestaurantMedia


class Restaurant(RegionMixin, Base):
    __tablename__ = "restaurants"

    name: Mapped[str]
    average_check: Mapped[int]
    description: Mapped[str] = mapped_column(Text, nullable=True)
    site_url: Mapped[str] = mapped_column(URLType, nullable=True)
    is_inner: Mapped[bool] = mapped_column(default=True)
    is_delivery: Mapped[bool] = mapped_column(default=False)
    rating: Mapped[float]
    priority: Mapped[float] = mapped_column(default=0)
    phone: Mapped[str] = mapped_column(
        PhoneNumberType(region="RU"), nullable=True
    )

    medias: Mapped[list[RestaurantMedia]] = relationship(
        cascade="all, delete-orphan"
    )

    cuisine_id: Mapped[int] = mapped_column(
        ForeignKey('restaurant_cuisines.id'), nullable=True
    )
    cuisine: Mapped[RestaurantCuisine] = relationship(foreign_keys=cuisine_id)

    vk: Mapped[str] = mapped_column(URLType, nullable=True)
    instagram: Mapped[str] = mapped_column(URLType, nullable=True)
    whatsapp: Mapped[str] = mapped_column(URLType, nullable=True)
    telegram: Mapped[str] = mapped_column(URLType, nullable=True)

    def to_list_dto(self) -> dto.ListRestaurant:
        return dto.ListRestaurant(
            id_=self.id,
            name=self.name,
            rating=self.rating,
            priority=self.priority,
            site_url=self.site_url,
            phone=self.phone,
            cuisine=self.cuisine.to_dto(),
        )

    def to_dto(self) -> dto.Restaurant:
        return dto.Restaurant(
            id_=self.id,
            name=self.name,
            average_check=self.average_check,
            is_inner=self.is_inner,
            is_delivery=self.is_delivery,
            rating=self.rating,
            priority=self.priority,
            site_url=self.site_url,
            description=self.description,
            phone=self.phone,
            medias=[
                _media.to_dto()
                for _media in self.medias
            ],
            cuisine=self.cuisine.to_dto(),
            instagram=self.instagram,
            vk=self.vk,
            whatsapp=self.whatsapp,
            telegram=self.telegram,
        )
