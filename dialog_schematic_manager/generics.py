from enum import StrEnum
from typing import TypeVar

from aiogram_dialog.api.internal import WindowProtocol


WindowT = TypeVar("WindowT", bound=WindowProtocol, covariant=True, contravariant=False)


class ParamTypes(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    NONE = "none"
