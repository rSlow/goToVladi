from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class RestaurantCuisine(Base):
    __tablename__ = 'restaurant_cuisines'

    id_: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def to_dto(self) -> dto.RestaurantCuisine:
        return dto.RestaurantCuisine(
            id_=self.id_,
            name=self.name
        )
