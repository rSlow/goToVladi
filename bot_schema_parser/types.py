from enum import StrEnum
from typing import TypeVar

from aiogram_dialog.api.internal import WindowProtocol

SCHEMATIC_ATTR_NAME = "_window_schema"

SCHEMA_KEY = "_bot_schema"
BUILDER_KEY = "_data_builder"

DIRECT_BUTTON_PREFIX = "_S_"
LOADER_BUTTON_PREFIX = "__schema__"

WindowT = TypeVar("WindowT", bound=WindowProtocol, covariant=True, contravariant=False)


class ParamTypes(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    NONE = "none"
