from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDao


class SeaRecreationDao(BaseDao[db.SeaRecreation]):
    async def get_all_categories(self, region_id: int):
        result = await self.session.scalars(
            select(db.SeaRecreationCategory)
            .join(self.model)
            .where(self.model.region_id == region_id)
            .distinct()
        )
        categories = result.all()
        return [category.to_dto() for category in categories]
    async def get_category(self, category_id: int):
        result = await self.session.scalars(
            select(db.SeaRecreationCategory)
            .where(db.SeaRecreationCategory.id == category_id)
        )
        return result.one().to_dto()

    async def get_filtered_list(self, category_id: int) -> list[dto.ListHotel]:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.category_id == category_id)
            .options(*get_list_sea_recreation_options())
        )
        return [sea_recreation.to_list_dto() for sea_recreation in result.all()]

    async def get(self, id_: int) -> dto.Hotel:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_sea_recreation_options())
        )
        return result.one().to_dto()


def get_list_sea_recreation_options():
    return (
        joinedload(db.SeaRecreation.category),
        joinedload(db.SeaRecreation.region),
    )


def get_sea_recreation_options():
    return (
        *get_list_sea_recreation_options(),
        selectinload(db.SeaRecreation.medias),
    )
