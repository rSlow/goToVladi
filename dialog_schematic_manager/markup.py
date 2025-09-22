from abc import abstractmethod
from enum import Enum
from typing import Protocol, TypeVar

from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder

MarkupButton = TypeVar("MarkupButton", InlineKeyboardButton, KeyboardButton)
MarkupButtonType = type[MarkupButton]
KeyboardMarkup = InlineKeyboardMarkup | ReplyKeyboardMarkup


class BaseMarkupFactory(Protocol):
    @property
    @abstractmethod
    def builder(self) -> KeyboardBuilder: ...

    @property
    @abstractmethod
    def button_class(self) -> MarkupButtonType: ...


class ReplyMarkupFactory(BaseMarkupFactory):
    @property
    def builder(self):
        return ReplyKeyboardBuilder()

    @property
    def button_class(self):
        return KeyboardButton


class InlineMarkupFactory(BaseMarkupFactory):
    @property
    def builder(self):
        return InlineKeyboardBuilder()

    @property
    def button_class(self):
        return InlineKeyboardButton


class MarkupFactoryEnum(Enum):
    REPLY = ReplyMarkupFactory()
    INLINE = InlineMarkupFactory()
