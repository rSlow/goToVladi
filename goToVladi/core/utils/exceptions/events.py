from aiogram import types as t

from .base import BaseError


class UnknownEventTypeError(BaseError):
    message = "Неподдерживаемый тип события."

    def __init__(self, event: t.TelegramObject):
        super().__init__()
        self.event = event
