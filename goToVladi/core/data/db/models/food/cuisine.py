from sqlalchemy.orm import Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class FoodCuisine(Base):
    __tablename__ = 'restaurant_cuisines'

    name: Mapped[str]

    def __str__(self):
        return f"{self.name} кухня"

    def to_dto(self) -> dto.FoodCuisine:
        return dto.FoodCuisine.model_validate(self)
