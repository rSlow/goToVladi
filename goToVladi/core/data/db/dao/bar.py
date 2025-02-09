from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class BarDao(BaseDao[db.Bar]):
    async def get_all_from_region(self, region_id: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.region_id == region_id)
            .options(
                joinedload(self.model.region)
            )
        )
        return [bar.to_list_dto() for bar in result.all()]

    async def get(self, id_: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_bar_options())
        )
        return result.one().to_dto()


def get_bar_options():
    return (
        joinedload(db.Bar.region),
        selectinload(db.Bar.medias),
    )
