from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from bot_schema_parser.buttons import ApiButton
from bot_schema_parser.keyboard import ApiKeyboard


class ButtonFactory(StrEnum):
    REPLY = "REPLY"
    INLINE = "INLINE"


class ApiMessage(BaseModel):
    chat_ids: list[int]
    text: str
    keyboard: ApiKeyboard = Field(default_factory=list)
    button_factory: ButtonFactory

    @field_validator("keyboard", mode="before")  # noqa
    @classmethod
    def validate_keyboard(cls, keyboard: dict) -> ApiKeyboard:
        return \
            [
                [
                    ApiButton.get_model_class(button["type_name"]).model_validate(button)
                    for button in row
                ]
                for row in keyboard
            ]
