from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class BaseCardMixin:
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def to_list_dto(self):
        raise NotImplementedError

    def to_dto(self):
        raise NotImplementedError
