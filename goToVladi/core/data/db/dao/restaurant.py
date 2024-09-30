from fastapi import UploadFile
from sqlalchemy import ScalarResult, select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.bot.utils.media import as_aiogram_content_type
from goToVladi.core.data.db import dto
from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDAO


class RestaurantDao(BaseDAO[db.Restaurant]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Restaurant, session)

    async def get_all_cuisines(self) -> list[db.RestaurantCuisine]:
        result: ScalarResult[db.RestaurantCuisine] = await self.session.scalars(
            select(db.RestaurantCuisine)
        )
        cuisines = result.all()
        return [cuisine.to_dto() for cuisine in cuisines]

    async def get_filtered_list(
            self, cuisine_id: int, is_delivery: bool, is_inner: bool
    ) -> list[dto.ListRestaurant]:
        result: ScalarResult[db.Restaurant] = await self.session.scalars(
            select(db.Restaurant)
            .where(db.Restaurant.cuisine_id == cuisine_id)
            .where(or_(
                db.Restaurant.is_inner == is_inner,
                db.Restaurant.is_delivery == is_delivery
            ))
            .options(*get_restaurant_list_options())
        )
        restaurants = result.all()
        return [restaurant.to_list_dto() for restaurant in restaurants]

    async def get(self, id_: int) -> dto.Restaurant:
        result: ScalarResult[db.Restaurant] = await self.session.scalars(
            select(db.Restaurant)
            .where(db.Restaurant.id == id_)
            .options(*get_restaurant_options())
        )
        return result.one().to_dto()

    async def add(self, restaurant: db.Restaurant) -> dto.Restaurant:
        self.session.add(restaurant)
        await self.session.commit()
        await self.session.refresh(restaurant, attribute_names=["id"])
        return await self.get(restaurant.id)

    async def add_medias(self, restaurant_id: int, *medias: UploadFile) -> bool:
        self.session.add_all([
            db.RestaurantMedia(
                restaurant_id=restaurant_id,
                content_type=as_aiogram_content_type(media.content_type),
                content=media
            )
            for media in medias
        ])
        await self.session.commit()
        return True

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            delete(db.Restaurant)
            .where(db.Restaurant.id == id_)
        )
        await self.session.commit()


def get_restaurant_list_options():
    return (
        joinedload(db.Restaurant.cuisine),
    )


def get_restaurant_options():
    return (
        *get_restaurant_list_options(),
        selectinload(db.Restaurant.medias),
    )
