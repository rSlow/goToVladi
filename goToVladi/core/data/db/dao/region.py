from sqlalchemy.ext.asyncio import AsyncSession

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDAO


class RegionDao(BaseDAO[db.Region]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Region, session)

    def get(self, id_: int):
        ...
