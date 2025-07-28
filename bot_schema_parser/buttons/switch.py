from typing import Any

from bot_schema_parser.buttons.actionable import ActionableButtonProtocol
from bot_schema_parser.buttons.base import BuildingButton
from bot_schema_parser.buttons.types import AiogramButtonType, AiogramButton
from bot_schema_parser.data_param import DataParamIn


class SwitchStateButton(BuildingButton, ActionableButtonProtocol):
    __type_key__ = "switch_state"
    __type_annotation__ = "Переключение на окно"

    state: str
    start_data: list[DataParamIn] | None = None
    dialog_data: list[DataParamIn] | None = None

    def action(self, child_of_target: Any):
        ...

    @classmethod
    def as_aiogram_button(cls, data: str, button_class: AiogramButtonType) -> AiogramButton:
        ...
