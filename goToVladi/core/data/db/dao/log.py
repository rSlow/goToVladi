from sqlalchemy import select, desc

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao.base import BaseDao


class EventLogDao(BaseDao[db.LogEvent]):
    async def get_last_by_user(self, user_id: int, data: str | None) -> dto.LogEvent | None:
        q = (select(self.model)
             .where(self.model.user_id == user_id)
             .order_by(desc(self.model.dt))
             .limit(1))
        if data is not None:
            q = q.where(self.model.data == data)
        res = await self.session.scalars(q)
        event = res.one_or_none()
        if event:
            return event.to_dto()

    async def write_event(self, event: dto.LogEvent) -> None:
        self.session.add(
            db.LogEvent(
                event_type=event.event_type,
                chat_id=event.chat_id,
                dt=event.dt,
                user_id=event.user_id,
                content_type=event.content_type,
                data=event.data
            )
        )
        await self.commit()
