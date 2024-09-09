from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.types.converted_integer import ConvertedInteger


class RestaurantCuisine(Base):
    __tablename__ = 'restaurant_cuisines'

    id: Mapped[int] = mapped_column(ConvertedInteger, primary_key=True)
    name: Mapped[str]

    def __str__(self):
        return f"{self.name} кухня"

    def to_dto(self) -> dto.RestaurantCuisine:
        return dto.RestaurantCuisine(
            id_=self.id,
            name=self.name
        )
