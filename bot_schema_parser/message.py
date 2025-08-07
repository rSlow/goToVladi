from pydantic import BaseModel, Field, field_validator

from bot_schema_parser.buttons import ApiButton
from bot_schema_parser.keyboard import ApiKeyboard
from bot_schema_parser.markup import MarkupFactoryEnum


class ApiMessage(BaseModel):
    chat_ids: list[int]
    text: str
    keyboard: ApiKeyboard = Field(default_factory=list)
    button_factory: MarkupFactoryEnum

    @field_validator("keyboard", mode="before")  # noqa
    @classmethod
    def validate_keyboard(cls, keyboard: dict) -> ApiKeyboard:
        return \
            [
                [
                    ApiButton.init_from_dict_config(button)
                    for button in row
                ]
                for row in keyboard
            ]
