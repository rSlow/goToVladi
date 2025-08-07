from pydantic import AnyHttpUrl

from bot_schema_parser.buttons.base import RawButton
from bot_schema_parser.markup import MarkupButtonType, MarkupButton, MarkupFactoryEnum


class UrlButton(RawButton):
    __type_key__ = "url"
    __type_annotation__ = "Ссылка"
    __markup_factories__ = [MarkupFactoryEnum.INLINE]

    url: AnyHttpUrl

    def as_aiogram_button(
            self, button_class: MarkupButtonType, button_data: str | None = None
    ) -> MarkupButton:
        return button_class(text=self.text, url=str(self.url))
