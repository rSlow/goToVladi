from fastadmin import SqlAlchemyModelAdmin
from passlib.context import CryptContext
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import async_sessionmaker as maker, AsyncSession

from goToVladi.core.data.db.models import User


class UserAdmin(SqlAlchemyModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    async def authenticate(self, username: str, password: str):
        session_maker: maker[AsyncSession] = self.get_sessionmaker()
        async with session_maker() as session:
            result: ScalarResult[User] = await session.scalars(
                select(User).filter_by(username=username)
            )
            user = result.one_or_none()

        if not user or not user.is_superuser:
            return None

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user.id
