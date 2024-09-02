from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import URLType

from ..base import Base


class RestaurantPhoto(Base):
    __tablename__ = 'restaurant_photos'

    id: Mapped[int] = mapped_column(primary_key=True)
    url = mapped_column(URLType)
