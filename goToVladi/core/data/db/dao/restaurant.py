from sqlalchemy import ScalarResult, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from goToVladi.core.data.db import dto, forms
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

    async def get_all(
            self, cuisine_id: int, type_: dto.RestaurantType
    ) -> list[dto.Restaurant]:
        result: ScalarResult[db.Restaurant] = await self.session.scalars(
            select(db.Restaurant)
            .where(db.Restaurant.cuisine_id == cuisine_id)
            .where(db.Restaurant.type_ == type_)
            .options(*get_restaurants_options())
        )
        restaurants = result.all()
        return [restaurant.to_dto() for restaurant in restaurants]

    async def get(self, id_: int) -> dto.Restaurant:
        result: ScalarResult[db.Restaurant] = await self.session.scalars(
            select(db.Restaurant)
            .where(db.Restaurant.id == id_)
            .options(*get_restaurants_options())
        )
        return result.one().to_dto()

    async def add(
            self, restaurant: forms.RestaurantInputForm
    ) -> dto.Restaurant:
        restaurant_db = db.Restaurant(
            name=restaurant.name,
            average_check=restaurant.average_check,
            type_=restaurant.type_,
            rating=restaurant.rating,
            cuisine_id=restaurant.cuisine_id,
            photos=restaurant.photos,
            priority=restaurant.priority,
            site_url=restaurant.site_url,
            description=restaurant.description,
            phone=restaurant.phone,
            vk=restaurant.vk,
            instagram=restaurant.instagram,
            whatsapp=restaurant.whatsapp,
            telegram=restaurant.telegram
        )
        self.session.add(restaurant_db)
        await self.session.commit()
        await self.session.refresh(restaurant_db, attribute_names=["id"])
        return await self.get(restaurant_db.id)

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            delete(db.Restaurant)
            .where(db.Restaurant.id == id_)
        )
        await self.session.commit()


def get_restaurants_options():
    return (
        joinedload(db.Restaurant.cuisine),
    )
