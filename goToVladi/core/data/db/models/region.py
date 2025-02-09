from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class Region(Base):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(unique=True)

    def to_dto(self) -> dto.Region:
        return dto.Region.model_validate(self)

    def __str__(self):
        return self.name
