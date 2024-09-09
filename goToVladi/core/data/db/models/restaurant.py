from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from .restaurant_cuisine import RestaurantCuisine
from ..types.string_phonenumber import StringPhoneNumberType


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    average_check: Mapped[int]
    description = mapped_column(Text, nullable=True)
    site_url: Mapped[str] = mapped_column(nullable=True)
    type_: Mapped[dto.RestaurantType] = mapped_column(
        default=dto.RestaurantType.INNER,
    )
    rating: Mapped[float]
    priority: Mapped[float] = mapped_column(default=0)
    phone: Mapped[str] = mapped_column(StringPhoneNumberType)

    photo: Mapped[str] = mapped_column(nullable=True)

    cuisine_id: Mapped[int] = mapped_column(
        ForeignKey('restaurant_cuisines.id'), nullable=True
    )
    cuisine: Mapped[RestaurantCuisine] = relationship(foreign_keys=cuisine_id)

    vk = mapped_column(URLType, nullable=True)
    instagram = mapped_column(URLType, nullable=True)
    whatsapp = mapped_column(URLType, nullable=True)
    telegram = mapped_column(URLType, nullable=True)

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
            phone=self.phone,
            photos=[self.photo],
            cuisine=self.cuisine.to_dto(),
            instagram=self.instagram,
            vk=self.vk,
            whatsapp=self.whatsapp,
            telegram=self.telegram,
        )

    def __str__(self):
        return f"{self.name} {self.site_url}"
