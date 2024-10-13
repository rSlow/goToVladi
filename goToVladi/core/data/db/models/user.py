from sqlalchemy import BigInteger, ForeignKey, sql
from sqlalchemy.orm import mapped_column, Mapped, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base, Region
from goToVladi.core.data.db.models.mixins.time import TimeMixin


class User(TimeMixin, Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}  # TODO eager_defaults

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    hashed_password: Mapped[str | None]
    is_bot: Mapped[bool] = mapped_column(
        default=False, server_default=sql.false()
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False, server_default=sql.false()
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=sql.true()
    )

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="SET NULL"), nullable=True
    )
    region: Mapped[Region] = relationship(foreign_keys=region_id)

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
            id_=self.id,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            is_bot=self.is_bot,
            is_superuser=self.is_superuser,
            region=self.region.to_dto() if self.region else None
        )
