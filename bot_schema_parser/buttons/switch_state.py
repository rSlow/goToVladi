from bot_schema_parser.buttons.base import ActionableButton
from bot_schema_parser.data_param import DataParamIn
from bot_schema_parser.markup import MarkupButtonType, MarkupButton, MarkupFactoryEnum


class SwitchStateButton(ActionableButton):
    __type_key__ = "switch_state"
    __type_annotation__ = "Переключение на окно"
    __markup_factories__ = [MarkupFactoryEnum.REPLY, MarkupFactoryEnum.INLINE]

    state: str
    start_data: list[DataParamIn] | None = None
    dialog_data: list[DataParamIn] | None = None

    def as_aiogram_button(
            self, button_class: MarkupButtonType, button_data: str | None = None
    ) -> MarkupButton:
        pass

    def action(self):
        pass
