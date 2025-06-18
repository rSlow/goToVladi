from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.models import Base
from goToVladi.core.data.db.utils.dto_validation import dto_validate

UsersRoles = Table(
    "users_roles",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "role_id",
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    ),
)


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)
    alias: Mapped[str]
    users = relationship(
        "User", secondary=UsersRoles,
        back_populates="roles", uselist=True,
    )
    to_dto = dto_validate(dto.UserRole)

    def __str__(self):
        return self.alias

    # def to_dto(self):
    #     return dto.UserRole.model_validate(self)
