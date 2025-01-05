from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDao


class CarRentDao(BaseDao[db.CarRent]):
    async def get_all_car_classes(self, region_id: int):
        result: ScalarResult[db.CarClass] = await self.session.scalars(
            select(db.CarClass)
            .join(db.CarRentsClasses)
            .join(db.CarRent)
            .where(db.CarRent.region_id == region_id)
            .distinct()
        )
        return [rent.to_dto() for rent in result.all()]

    async def get_all_rents_in_class(self, car_class_id: int, region_id: int):
        result: ScalarResult[db.CarRent] = await self.session.scalars(
            select(self.model)
            .join(db.CarRentsClasses)
            .where(db.CarRentsClasses.columns.car_class_id == car_class_id)
            .where(self.model.region_id == region_id)
            .options(
                # selectinload(db.CarRentsClasses),
                joinedload(self.model.region)
            )
        )
        return [rent.to_list_dto() for rent in result.all()]

    async def get_car_class(self, car_class_id: int):
        res = await self.session.scalars(
            select(db.CarClass)
            .where(db.CarClass.id == car_class_id)
        )
        return res.one().to_dto()

    async def get(self, id_: int) -> dto.CarRent:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(
                joinedload(self.model.region),
                selectinload(self.model.medias),
                selectinload(self.model.car_classes)
            )
        )
        return result.one().to_dto()
