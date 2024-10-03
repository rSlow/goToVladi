from sqlalchemy.orm import Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class RestaurantCuisine(Base):
    __tablename__ = 'restaurant_cuisines'

    name: Mapped[str]
    restaurants = relationship("Restaurant", back_populates="cuisine")

    def __str__(self):
        return f"{self.name} кухня"

    def to_dto(self) -> dto.RestaurantCuisine:
        return dto.RestaurantCuisine(
            id_=self.id,
            name=self.name
        )
