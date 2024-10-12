from aiogram import types as t

from goToVladi.core.utils.exceptions.base import BaseError


class UnknownEventTypeError(BaseError):
    message = "Неподдерживаемый тип события: {event}"

    def __init__(self, event: t.TelegramObject):
        super().__init__(event=event)


class UnknownContentTypeError(BaseError):
    message = "Неизвестный тип файла: {file_content_type}"

    def __init__(self, file_content_type: str):
        super().__init__(file_content_type=file_content_type)
