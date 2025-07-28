from pydantic import AnyHttpUrl

from bot_schema_parser.buttons.base import RawButton


class UrlButton(RawButton):
    __type_key__ = "url"
    __type_annotation__ = "Ссылка"

    url: AnyHttpUrl
