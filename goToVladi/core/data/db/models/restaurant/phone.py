from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import PhoneNumberType

from ..base import Base


class RestaurantPhone(Base):
    __tablename__ = 'restaurant_phones'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone = mapped_column(PhoneNumberType(region="RU"))
