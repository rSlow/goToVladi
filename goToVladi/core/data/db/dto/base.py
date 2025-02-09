from pydantic import BaseModel

from goToVladi.core.data.db.dto.mixins import ORMMixin


class BaseDto(BaseModel, ORMMixin):
    id: int | None = None


class BaseListCardDto(BaseDto):
    name: str


class BaseCardDto(BaseDto):
    name: str
    description: str | None = None
