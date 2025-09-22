from pydantic import BaseModel

from goToVladi.core.data.db.dto.mixins import ORMMixin


class Setting(BaseModel, ORMMixin):
    _id: int
    key: str
    value: str
