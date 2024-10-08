from dishka import AsyncContainer
from fastadmin import register_admin_model_class as register
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from goToVladi.core.data.db.models import User, Restaurant, RestaurantCuisine
from .restaurant import RestaurantModelAdmin, RestaurantCuisineModelAdmin
from .user import UserAdmin


async def register_models(dishka: AsyncContainer):
    session_maker: async_sessionmaker[AsyncSession] = await dishka.get(
        async_sessionmaker[AsyncSession]
    )
    register(UserAdmin, [User], sqlalchemy_sessionmaker=session_maker)
    register(
        RestaurantModelAdmin,
        [Restaurant],
        sqlalchemy_sessionmaker=session_maker
    )
    register(
        RestaurantCuisineModelAdmin,
        [RestaurantCuisine],
        sqlalchemy_sessionmaker=session_maker
    )
