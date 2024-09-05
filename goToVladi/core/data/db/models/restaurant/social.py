from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class RestaurantSocial(Base):
    __tablename__ = 'restaurant_socials'

    id_: Mapped[int] = mapped_column(primary_key=True)
    url = mapped_column(URLType)

    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    restaurant = relationship(
        "Restaurant",
        foreign_keys=restaurant_id,
        back_populates="socials",
    )

    def to_dto(self) -> dto.RestaurantSocial:
        return dto.RestaurantSocial(
            id_=self.id_,
            url=self.url
        )
