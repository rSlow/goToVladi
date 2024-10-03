from fastapi import UploadFile
from sqlalchemy import ScalarResult, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDAO


class HotelDao(BaseDAO[db.Hotel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Hotel, session)

    async def get_all_districts(self, region_id: int):
        result: ScalarResult[db.HotelDistrict] = await self.session.scalars(
            select(db.HotelDistrict)
            .where(db.HotelDistrict.region_id == region_id)
            .options(joinedload(db.HotelDistrict.region))
        )
        hotel_districts = result.all()
        return [district.to_dto() for district in hotel_districts]

    async def get(self, id_: int) -> dto.Hotel:
        result: ScalarResult[db.Hotel] = await self.session.scalars(
            select(db.Hotel)
            .where(db.Hotel.id == id_)
            .options(*get_hotel_options())
        )
        return result.one().to_dto()

    async def get_filtered_list(self, district_id: str) -> list[dto.ListHotel]:
        result: ScalarResult[db.Hotel] = await self.session.scalars(
            select(db.Hotel)
            .where(db.Hotel.district_id == district_id)
            .options(*get_hotel_options())
        )
        hotels = result.all()
        return [hotel.to_list_dto() for hotel in hotels]

    async def add(self, hotel: db.Hotel) -> dto.Hotel:
        self.session.add(hotel)
        await self.session.commit()
        await self.session.refresh(hotel, attribute_names=["id"])
        return await self.get(hotel.id)

    async def add_medias(self, hotel_id: int, *medias: UploadFile) -> bool:
        self.session.add_all([
            db.HotelMedia(hotel_id=hotel_id, content=media)
            for media in medias
        ])
        await self.session.commit()
        return True

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            delete(db.Hotel)
            .where(db.Hotel.id == id_)
        )
        await self.session.commit()


def get_hotel_options():
    return (
        selectinload(db.Hotel.medias),
        joinedload(db.Hotel.district).options(
            joinedload(db.HotelDistrict.region),
        ),
    )
