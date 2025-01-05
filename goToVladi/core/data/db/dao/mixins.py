from typing import TypeVar, Generic

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.core.data.db.dao.base import ModelType

DtoType = TypeVar("DtoType")


class BaseDaoMixin(Generic[DtoType]):
    session: AsyncSession
    model: ModelType
    _export_dto_type: type[DtoType]

    def __new__(cls, *args, **kwargs):
        dao = super().__new__(cls)
        dao._export_dto_type = dao.__orig_bases__[0].__args__[0]
        return dao

    def __init__(self):
        self._dto: type[DtoType] = type(self).__orig_bases__[0].__args__[0]


class GetListWithRegion(BaseDaoMixin[DtoType]):
    async def get_all_from_region(self, region_id: int) -> list[DtoType]:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.region_id == region_id)  # TODO сделать типизацию
            .options(
                joinedload(self.model.region)
            )
        )
        return [massage.to_list_dto() for massage in result.all()]


class GetWithRegionAndMedias(BaseDaoMixin[DtoType]):
    @property
    def options(self):
        return (
            joinedload(self.model.region),
            selectinload(self.model.medias),
        )

    async def get(self, id_: int) -> DtoType:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*self.options)
        )
        return result.one().to_dto()
