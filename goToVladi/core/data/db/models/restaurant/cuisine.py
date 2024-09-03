from sqlalchemy.orm import Mapped, mapped_column, relationship

from goToVladi.core.data.db.models import Base


class RestaurantCuisine(Base):
    __tablename__ = 'restaurant_cuisines'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
