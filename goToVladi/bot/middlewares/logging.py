import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram import types as t
from aiogram_dialog.api.entities import DialogUpdateEvent

from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.utils import events as get_event
from goToVladi.bot.utils.exceptions import (UnknownEventTypeError,
                                            PassEventException)
from goToVladi.core.data.db import dto

logger = logging.getLogger(__name__)


def _parse_event(event: t.TelegramObject) -> dto.LogEvent:
    if isinstance(event, t.Message):
        return get_event.from_message(event)
    elif isinstance(event, t.CallbackQuery):
        return get_event.from_callback_query(event)
    elif isinstance(event, DialogUpdateEvent):
        raise PassEventException(event)
    raise UnknownEventTypeError(event)


class EventLoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[t.TelegramObject, dict[str, Any]], Awaitable],
            event: t.TelegramObject,
            data: MiddlewareData
    ):
        try:
            event_dto = _parse_event(event)
            dao = data["dao"]
            await dao.log.write_event(event_dto)

        except UnknownEventTypeError as ex:
            logger.warning(ex)
        except PassEventException as ex:
            logger.debug(ex)

        return await handler(event, data)
