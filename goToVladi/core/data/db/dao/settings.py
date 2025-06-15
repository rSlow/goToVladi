from sqlalchemy import select

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class SettingsDao(BaseDao[db.Setting]):
    async def get_by_id(self, id_: int):
        message = await self._get_by_id(id_)
        return message.to_dto()

    async def get_by_key(self, key: str):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.key == key)
        )
        message = result.one()
        if message is not None:
            return message.to_dto()
