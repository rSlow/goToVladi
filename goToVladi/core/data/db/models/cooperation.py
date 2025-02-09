from sqlalchemy import Text, sql
from sqlalchemy.orm import Mapped, mapped_column

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.models.mixins.time import TimeMixin


class Cooperation(Base, TimeMixin):
    __tablename__ = "cooperations"

    user_tg_username: Mapped[str | None] = None
    text: Mapped[str] = mapped_column(Text)
    is_archived: Mapped[bool] = mapped_column(server_default=sql.false(), nullable=False)

    def to_dto(self):
        return dto.Cooperation.model_validate(self)
