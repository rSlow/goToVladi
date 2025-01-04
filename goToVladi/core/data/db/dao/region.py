from sqlalchemy.ext.asyncio import AsyncSession

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class RegionDao(BaseDao[db.Region]):
    async def get(self, id_: int):
        region = await self._get_by_id(id_)
        return region.to_dto()

    async def get_all(self):
        regions = await self._get_all()
        return [region.to_dto() for region in regions]
