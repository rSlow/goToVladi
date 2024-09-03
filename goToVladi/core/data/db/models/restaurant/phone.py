from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumberType

from goToVladi.core.data.db.models import Base


class RestaurantPhone(Base):
    __tablename__ = 'restaurant_phones'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone = mapped_column(PhoneNumberType(region="RU"))

    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    restaurant = relationship(
        "Restaurant",
        foreign_keys=restaurant_id,
        back_populates="phones",
    )
