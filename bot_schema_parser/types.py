from enum import StrEnum
from typing import TypeVar

from aiogram_dialog.api.internal import WindowProtocol

SCHEMATIC_ATTR_NAME = "_window_schema"

MANAGER_KEY = "_schema_manager"

WindowT = TypeVar("WindowT", bound=WindowProtocol, covariant=True, contravariant=False)


class ParamTypes(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    NONE = "none"
