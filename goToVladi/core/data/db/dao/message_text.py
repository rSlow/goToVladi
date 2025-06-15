from sqlalchemy import select

from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao


class MessageTextDao(BaseDao[db.MessageText]):
    async def get_by_id(self, id_: int):
        message = await self._get_by_id(id_)
        return message.to_dto()

    async def get_by_name(self, name: str):
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.name == name)
        )
        message = result.one_or_none()
        if message is not None:
            return message.to_dto()
