from pathlib import Path

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao.base import BaseDAO
from goToVladi.core.data.db.models.restaurant import Restaurant, \
    RestaurantCuisine


class RestaurantDao(BaseDAO[Restaurant]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Restaurant, session)

    async def get_all_cuisines(self) -> list[RestaurantCuisine]:
        result: ScalarResult[RestaurantCuisine] = await self.session.scalars(
            select(RestaurantCuisine)
        )
        cuisines = result.all()
        return [cuisine.to_dto() for cuisine in cuisines]

    async def get_restaurants(
            self, cuisine_id: int, type_: dto.RestaurantType
    ) -> list[dto.Restaurant]:
        result: ScalarResult[Restaurant] = await self.session.scalars(
            select(Restaurant)
            .where(Restaurant.cuisine_id == cuisine_id)
            .where(Restaurant.type_ == type_)
            .options(*get_restaurants_options())
        )
        restaurants = result.all()
        return [restaurant.to_dto() for restaurant in restaurants]

    async def get_restaurant(self, id_: int) -> dto.Restaurant:
        result: ScalarResult[Restaurant] = await self.session.scalars(
            select(Restaurant)
            .where(Restaurant.id == id_)
            .options(*get_restaurants_options())
        )
        return result.one().to_dto()

    async def save_restaurant_photo(self, id_: int, file_path: Path) -> None:
        restaurant = await self._get_by_id(id_)
        restaurant.photo = file_path.absolute().as_posix()
        await self.session.commit()


def get_restaurants_options():
    return (
        joinedload(Restaurant.cuisine),
    )
