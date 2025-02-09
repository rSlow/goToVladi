from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class MessageText(Base):
    __tablename__ = "message_texts"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    value: Mapped[str] = mapped_column(Text)

    def to_dto(self):
        return dto.MessageText.model_validate(self)
