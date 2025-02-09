from fastapi import UploadFile
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class RestaurantDao(BaseDao[db.Restaurant]):
    async def get_all_cuisines(self, region_id: int):
        result = await self.session.scalars(
            select(db.FoodCuisine)
            .join(self.model)
            .where(self.model.region_id == region_id)
            .distinct()
        )
        cuisines = result.all()
        return [cuisine.to_dto() for cuisine in cuisines]

    async def get_filtered_list(self, cuisine_id: int, region_id: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.cuisine_id == cuisine_id)
            .where(self.model.region_id == region_id)
            .options(*get_restaurant_list_options())
        )
        restaurants = result.all()
        return [restaurant.to_list_dto() for restaurant in restaurants]

    async def get(self, id_: int):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_restaurant_options())
        )
        return result.one().to_dto()

    async def add(self, restaurant: db.Restaurant):
        self.session.add(restaurant)
        await self.commit()
        await self.session.refresh(restaurant, attribute_names=["id"])
        return await self.get(restaurant.id)

    async def add_medias(self, restaurant_id: int, *medias: UploadFile) -> bool:
        self.session.add_all([
            db.RestaurantMedia(
                restaurant_id=restaurant_id, content=media  # type: ignore
            )
            for media in medias
        ])
        await self.commit()
        return True

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            delete(db.Restaurant)
            .where(db.Restaurant.id == id_)
        )
        await self.commit()


def get_restaurant_list_options():
    return (
        joinedload(db.Restaurant.cuisine),
        joinedload(db.Restaurant.region),
    )


def get_restaurant_options():
    return (
        *get_restaurant_list_options(),
        selectinload(db.Restaurant.medias),
    )
