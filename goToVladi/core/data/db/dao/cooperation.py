from goToVladi.core.data.db import models as db
from goToVladi.core.data.db.dao.base import BaseDao
from goToVladi.core.data.db.models import Cooperation


class CooperationDao(BaseDao[db.Cooperation]):
    async def add(self, text: str, username: str | None = None):
        self.session.add(
            Cooperation(text=text, user_tg_username=username)
        )
        await self.commit()
