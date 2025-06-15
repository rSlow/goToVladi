from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str] = mapped_column(Text)

    def to_dto(self):
        return dto.Setting.model_validate(self)
