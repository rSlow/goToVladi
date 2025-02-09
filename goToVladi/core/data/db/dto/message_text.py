from pydantic import BaseModel

from goToVladi.core.data.db.dto.mixins import ORMMixin


class MessageText(BaseModel, ORMMixin):
    _id: int
    name: str
    description: str
    value: str
