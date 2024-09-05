from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from goToVladi.core.data.db.dao.base import BaseDAO
from goToVladi.core.data.db.models.restaurant import Restaurant, \
    RestaurantCuisine


class RestaurantDao(BaseDAO[Restaurant]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Restaurant, session)

    async def get_all_cuisines(self) -> list[RestaurantCuisine]:
        result: ScalarResult[RestaurantCuisine] = await self.session \
            .scalars(select(RestaurantCuisine))
        cuisines = result.all()
        return [cuisine.to_dto() for cuisine in cuisines]

    async def get_cuisine_restaurants(
            self, cuisine_id: int
    ) -> list[Restaurant]:
        result: ScalarResult[Restaurant] = await self.session.scalars(
            select(Restaurant)
            .where(Restaurant.cuisine_id == cuisine_id)
        )
        restaurants = result.all()
        return [restaurant.to_dto() for restaurant in restaurants]

    async def get_restaurant(self, id_: int) -> Restaurant:
        restaurant = await self._get_by_id(id_)
        return restaurant.to_dto()
