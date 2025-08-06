from abc import abstractmethod
from typing import Protocol

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder

from . import BotSchema
from .buttons.base import ApiButton, BuildingButton, RawButton
from .buttons.types import InlineButtonActions, ReplyButtonActions, AiogramButtonType, \
    ButtonActionsEnum
from .data_builder import BaseDataBuilder
from .message import ApiMessage, ApiKeyboard, ButtonFactory
from .sender import SendExecutor, default_send_executor


class ButtonBuilder:
    def __init__(self):
        ...


ButtonClassTypeError = TypeError("button_class_type must be InlineKeyboardButton or KeyboardButton")


class BaseMarkupFactory(Protocol):
    @property
    @abstractmethod
    def builder(self) -> KeyboardBuilder: ...

    @property
    @abstractmethod
    def button_class(self) -> AiogramButtonType: ...

    @property
    @abstractmethod
    def button_actions(self) -> ButtonActionsEnum: ...


class ReplyMarkupFactory(BaseMarkupFactory):
    @property
    def builder(self):
        return ReplyKeyboardBuilder()

    @property
    def button_class(self):
        return KeyboardButton

    @property
    def button_actions(self):
        return ReplyButtonActions


class InlineMarkupFactory(BaseMarkupFactory):
    @property
    def builder(self):
        return InlineKeyboardBuilder()

    @property
    def button_class(self):
        return KeyboardButton

    @property
    def button_actions(self):
        return InlineButtonActions


class BotSchemaManager:
    def __init__(
            self,
            bot: Bot,
            bot_schema: BotSchema,
            data_builder: BaseDataBuilder,
            send_executor: SendExecutor,
    ):
        self._bot = bot
        self._bot_schema = bot_schema
        self._data_builder = data_builder
        self._send_executor = send_executor

        for schema in self._bot_schema.window_schemas:
            ...

    @staticmethod  # TODO
    def _get_markup_factory(button_factory_name: ButtonFactory) -> BaseMarkupFactory:
        if button_factory_name == ButtonFactory.REPLY:
            return ReplyMarkupFactory()
        elif button_factory_name == ButtonFactory.INLINE:
            return InlineMarkupFactory()

        raise ButtonClassTypeError  # TODO

    async def _create_aiogram_button(
            self,
            button: ApiButton,
            button_class: AiogramButtonType
    ):
        if isinstance(button, BuildingButton):
            button_data = await self._data_builder.create_data(button)
            return button.as_aiogram_button(button_data, button_class)
            # return button_class(**button.get_button_kwargs(button_data))
        if isinstance(button, RawButton):
            return button
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
            chat_ids=message.chat_id,
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

    async def handle_button(self, button_config: ApiButton):
        pass
