from sqlalchemy.orm import Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class SeaRecreationCategory(Base):
    __tablename__ = "sea_recreation_categories"
    name: Mapped[str]

    def to_dto(self):
        return dto.SeaRecreationCategory.model_validate(self)

    def __str__(self):
        return self.name
