from sqlalchemy import ScalarResult, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from .. import dto
from ..models.user import User


class UserDao(BaseDAO[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_tg_id(self, tg_id: int) -> dto.User:
        result: ScalarResult[User] = await self.session.scalars(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.one()
        return user.to_dto()

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = {
            "tg_id": user.tg_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_bot": user.is_bot,
        }
        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.tg_id,),
                set_=kwargs,
                where=User.tg_id == user.tg_id
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()
