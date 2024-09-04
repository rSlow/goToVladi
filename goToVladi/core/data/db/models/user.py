from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}  # TODO eager_defaults

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_bot: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        rez = (
            f"<User "
            f"id={self.id} "
            f"tg_id={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            is_bot=self.is_bot,
            is_superuser=self.is_superuser,
        )
