from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class BreakfastDao(BaseDao[db.Breakfast]):
    async def get_all_from_region(self, region_id: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.region_id == region_id)
            .options(
                joinedload(self.model.region)
            )
        )
        return [breakfast.to_list_dto() for breakfast in result.all()]

    async def get(self, id_: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_breakfast_options())
        )
        return result.one().to_dto()


def get_breakfast_options():
    return (
        joinedload(db.Breakfast.region),
        selectinload(db.Breakfast.medias),
    )
