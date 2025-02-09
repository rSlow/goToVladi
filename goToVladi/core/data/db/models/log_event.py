from datetime import datetime

from sqlalchemy import DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class LogEvent(Base):
    __tablename__ = "log_events"

    event_type: Mapped[str]
    chat_id: Mapped[int] = mapped_column(BigInteger)
    dt: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    content_type: Mapped[str | None]
    data: Mapped[str | None]

    def to_dto(self) -> dto.LogEvent:
        return dto.LogEvent.model_validate(self)
