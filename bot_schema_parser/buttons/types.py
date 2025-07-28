from enum import StrEnum, auto
from typing import TypeVar

from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup

AiogramButton = TypeVar("AiogramButton", InlineKeyboardButton, KeyboardButton)
AiogramButtonType = type[AiogramButton]
KeyboardMarkup = InlineKeyboardMarkup | ReplyKeyboardMarkup


class ReplyButtonActions(StrEnum):
    SWITCH_STATE = auto()
    WEB_APP = auto()
    REQUEST_USER = auto()
    REQUEST_CHAT = auto()
    REQUEST_CONTACT = auto()
    REQUEST_LOCATION = auto()
    REQUEST_POLL = auto()


class InlineButtonActions(StrEnum):
    SWITCH_STATE = auto()
    WEB_APP = auto()
    URL = auto()
    LOGIN_URL = auto()
    COPY_TEXT = auto()
    PAY = auto()


ButtonActions = TypeVar("ButtonActions", ReplyButtonActions, InlineButtonActions)
ButtonActionsEnum = type[ButtonActions]
