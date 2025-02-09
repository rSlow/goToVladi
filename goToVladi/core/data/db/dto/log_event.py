from datetime import datetime

from goToVladi.core.data.db.dto.base import BaseDto


class LogEvent(BaseDto):
    event_type: str
    chat_id: int
    dt: datetime
    user_id: int | None = None
    content_type: str | None = None
    data: str | None = None
