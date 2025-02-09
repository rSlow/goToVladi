from goToVladi.core.data.db.dto.base import BaseDto
from goToVladi.core.data.db.dto.mixins import TimeMixin


class Cooperation(BaseDto, TimeMixin):
    user_tg_id: int
    user_tg_username: str | None = None
    text: str
    is_archived: bool
