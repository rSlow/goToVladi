from fastapi import UploadFile
from sqlalchemy import ScalarResult, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDao


class TripDao(BaseDao[db.Trip]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.Trip, session)

    async def get_filtered_list(self, region_id: int) -> list[dto.ListHotel]:
        result: ScalarResult[db.Trip] = await self.session.scalars(
            select(self.model)
            .where(self.model.region_id == region_id)
            .options(*get_trip_options())
        )
        trips = result.all()
        return [trip.to_list_dto() for trip in trips]

    async def get(self, id_: int) -> dto.Trip:
        result: ScalarResult[db.Trip] = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*get_trip_options())
        )
        return result.one().to_dto()

    async def add(self, trip: db.Trip) -> dto.Trip:
        self.session.add(trip)
        await self.commit()
        await self.session.refresh(trip, attribute_names=["id"])
        return await self.get(trip.id)

    async def add_medias(self, trip_id: int, *medias: UploadFile) -> bool:
        self.session.add_all([
            db.TripMedia(trip_id=trip_id, content=media)
            for media in medias
        ])
        await self.commit()
        return True

    async def delete(self, id_: int) -> None:
        await self.session.execute(
            delete(self.model)
            .where(self.model.id == id_)
        )
        await self.commit()


def get_trip_options():
    return (
        joinedload(db.Trip.region),
        selectinload(db.Trip.medias),
    )
