from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDAO


class HotelDao(BaseDAO[db.Hotel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Hotel, session)

    async def get_all_districts(self):
        result: ScalarResult[str] = await self.session.scalars(
            select(self.model.district).distinct()
        )
        return result.all()

    async def get(self, id_: int) -> dto.Hotel:
        result: ScalarResult[db.Hotel] = await self.session.scalars(
            select(db.Hotel)
            .where(db.Hotel.id == id_)
            .options(*get_hotel_options())
        )
        return result.one().to_dto()

    async def get_filtered_list(self, district: str) -> list[dto.ListHotel]:
        result: ScalarResult[db.Hotel] = await self.session.scalars(
            select(db.Hotel)
            .where(db.Hotel.district == district)
        )
        hotels = result.all()
        return [hotel.to_list_dto() for hotel in hotels]


def get_hotel_options():
    return (
        selectinload(db.Hotel.medias),
    )
