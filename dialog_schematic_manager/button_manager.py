from abc import abstractmethod
from typing import Protocol, Iterable

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder

from bot_schema_parser.buttons.base import ApiButton, BuildingButton, RawButton

from bot_schema_parser.data_builder import BaseDataBuilder
from bot_schema_parser.markup import MarkupFactoryEnum, BaseMarkupFactory
from bot_schema_parser.message import ApiMessage, ApiKeyboard
from bot_schema_parser.schematic import BotSchema
from bot_schema_parser.sender import SendExecutor, default_send_executor


class ButtonBuilder:
    def __init__(self):
        ...


ButtonClassTypeError = TypeError("button_class_type must be InlineKeyboardButton or KeyboardButton")


class BotButtonManager:
    def __init__(
            self,
            bot: Bot,
            bot_schema: BotSchema,
            data_builder: BaseDataBuilder,
            send_executor: SendExecutor = default_send_executor,
    ):
        self._bot = bot
        self._bot_schema = bot_schema
        self._data_builder = data_builder
        self._send_executor = send_executor
        self._button_types: list[str, type[ApiButton]] = {}

        for schema in self._bot_schema.window_schemas:
            ...

    @staticmethod  # TODO
    def _get_markup_factory(button_factory_name: ButtonFactory) -> BaseMarkupFactory:
        try:
            return MarkupFactoryEnum[button_factory_name].value
        except KeyError:
            raise ButtonClassTypeError  # TODO

    async def _create_aiogram_button(
            self,
            button: ApiButton,
            button_class: AiogramButtonType
    ):
        if isinstance(button, BuildingButton):
            button_data = await self._data_builder.create_data(button)
            return button.as_aiogram_button(button_class, button_data)
            # return button_class(**button.get_button_kwargs(button_data))
        if isinstance(button, RawButton):
            return button.as_aiogram_button(button_class)
        raise TypeError("")  # TODO unknown button type

    async def _create_markup(self, keyboard: ApiKeyboard, button_factory: ButtonFactory):
        markup_factory = self._get_markup_factory(button_factory)
        markup_builder = markup_factory.builder
        for row in keyboard:
            markup_row = []
            for button in row:
                markup_row.append(
                    await self._create_aiogram_button(button, markup_factory.button_class)
                )
            markup_builder.row(*markup_row)
        return markup_builder.as_markup()

    async def handle_message(self, message: ApiMessage):
        markup = await self._create_markup(message.keyboard, message.button_factory)
        await self._send_executor(
            bot=self._bot,
            chat_ids=message.chat_ids,
            text=message.text,
            markup=markup
        )

    @staticmethod  # TODO
    def get_possible_button_types(button_class_type: AiogramButtonType):
        if button_class_type == InlineKeyboardButton:
            return [t.value for t in InlineButtonActions]
        if button_class_type == KeyboardButton:
            return [t.value for t in ReplyButtonActions]
        raise ButtonClassTypeError

    async def handle_button(self, button: ApiButton):
        await button.execute(
            self._bot,
            self._bot_schema
        )

    def register_buttons(self, buttons: Iterable[ApiButton]):
        for button in buttons:
            self._button_types[button.type_key] = button

    def with_send_executor(self, send_executor: SendExecutor):
        self._send_executor = send_executor
