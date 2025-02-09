from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class DeliveryDao(BaseDao[db.Delivery]):
    async def get_all_cuisines(self, region_id: int):
        result = await self.session.scalars(
            select(db.FoodCuisine)
            .join(self.model)
            .where(self.model.region_id == region_id)
            .distinct()
        )
        cuisines = result.all()
        return [cuisine.to_dto() for cuisine in cuisines]

    async def get_list_by_cuisine(self, cuisine_id: int, region_id: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.cuisine_id == cuisine_id)
            .where(self.model.region_id == region_id)
            .options(*get_delivery_list_options())
        )
        deliveries = result.all()
        return [delivery.to_list_dto() for delivery in deliveries]

    async def get(self, id_: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_delivery_options())
        )
        return result.one().to_dto()


def get_delivery_list_options():
    return (
        joinedload(db.Delivery.cuisine),
        joinedload(db.Delivery.region),
    )


def get_delivery_options():
    return (
        *get_delivery_list_options(),
        selectinload(db.Delivery.medias),
    )
