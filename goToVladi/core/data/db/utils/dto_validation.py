from typing import TypeVar

from goToVladi.core.data.db.dto.base import BaseDto
from goToVladi.core.data.db.models import Base

ValidatedModel = TypeVar("ValidatedModel", bound=Base, covariant=True, contravariant=False)
DtoType = TypeVar("DtoType", bound=BaseDto, covariant=True, contravariant=False)


def dto_validate(dto_model: type[DtoType]):
    def _model_validate(self: ValidatedModel) -> DtoType:
        return dto_model.model_validate(self)

    return _model_validate
