from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class Region(Base):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(unique=True)

    def to_dto(self) -> dto.Region:
        return dto.Region(
            id_=self.id,
            name=self.name
        )
