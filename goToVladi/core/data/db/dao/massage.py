from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class MassageDao(BaseDao[db.Massage]):
    async def get_all_from_region(self, region_id: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.region_id == region_id)  # TODO сделать типизацию
            .options(
                joinedload(self.model.region)
            )
        )
        return [massage.to_list_dto() for massage in result.all()]

    async def get(self, id_: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_massage_options())
        )
        return result.one().to_dto()


def get_massage_options():
    return (
        joinedload(db.Massage.region),
        selectinload(db.Massage.medias),
    )
