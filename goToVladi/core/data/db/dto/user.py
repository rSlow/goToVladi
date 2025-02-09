from aiogram import types as tg

from goToVladi.core.data.db.dto import Region
from goToVladi.core.data.db.dto.base import BaseDto
from goToVladi.core.utils.auth.models import FlaskLoginMixin


class User(BaseDto, FlaskLoginMixin):
    tg_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
    region: Region | None = None

    @property
    def fullname(self) -> str:
        if self.first_name is None:
            return ""
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def name_mention(self) -> str:
        return (self.fullname
                or self.username
                or str(self.tg_id)
                or str(self.id)
                or "unknown")

    @classmethod
    def from_aiogram(cls, user: tg.User) -> "User":
        return cls(
            tg_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_bot=user.is_bot,
            is_active=True
        )

    def with_password(self, hashed_password: str) -> "UserWithCreds":
        user_data = self.model_dump()
        user_data["hashed_password"] = hashed_password
        return UserWithCreds.model_validate(user_data)


class UserWithCreds(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        user_data = self.model_dump(exclude={"hashed_password"})
        return User.model_validate(user_data)
