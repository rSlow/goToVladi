from collections.abc import Sequence
from typing import TypeVar, Generic

from sqlalchemy import delete, func, ScalarResult
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from goToVladi.core.data.db.models.base import Base
from goToVladi.core.utils.functools import get_generic_types

ModelType = TypeVar(
    "ModelType", bound=Base, covariant=True, contravariant=False
)


class BaseDao(Generic[ModelType]):
    def __init__(self, session: AsyncSession) -> None:
        self.model: type[ModelType] = get_generic_types(type(self), 0)[0]
        self.session = session

    async def _get_all(self) -> Sequence[ModelType]:
        result: ScalarResult[ModelType] = await self.session.scalars(
            select(self.model)
        )
        return result.all()

    async def _get_by_id(self, id_: int) -> ModelType:
        result = await self.session.get(self.model, id_)
        if result is None:
            raise NoResultFound
        return result

    def _save(self, obj: ModelType):
        self.session.add(obj)

    async def delete_all(self):
        await self.session.execute(delete(self.model))

    async def _delete(self, obj: ModelType):
        await self.session.delete(obj)

    async def count(self):
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

    async def _flush(self, *objects: ModelType):
        await self.session.flush(objects)
