from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumberType, PhoneNumber

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class RestaurantPhone(Base):
    __tablename__ = 'restaurant_phones'

    id_: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[PhoneNumber] = mapped_column(PhoneNumberType(region="RU"))

    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    restaurant = relationship(
        "Restaurant",
        foreign_keys=restaurant_id,
        back_populates="phones",
    )

    def to_dto(self) -> dto.RestaurantPhone:
        return dto.RestaurantPhone(
            id_=self.id_,
            phone=self.phone
        )
