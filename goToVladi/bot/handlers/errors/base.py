import json
import logging
import typing as t
from functools import partial

from aiogram import Bot
from aiogram.exceptions import AiogramError
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd

from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.utils.exceptions.base import BaseError

logger = logging.getLogger(__name__)


async def bot_blocked(error: ErrorEvent, dao: DaoHolder):
    message = error.update.message or error.update.callback_query.message
    user_id = message.from_user.id
    await dao.user.deactivate(user_id)
    logger.info("Deactivated user with id %s", user_id)


# TODO check
async def handle_base_error(error: ErrorEvent, log_chat_id: int, bot: Bot):
    exception: BaseError = t.cast(BaseError, error.exception)
    if callback := error.update.callback_query:
        await callback.answer(exception.message, show_alert=True)
    else:
        chat_id = exception.chat_id or exception.user_id
        if chat_id is None and exception.user:
            chat_id = exception.user.tg_id

        if chat_id:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"Произошла ошибка\n{exception}"
                )
            except AiogramError as ex:
                logger.exception(
                    "can't send error message to user",
                    exc_info=ex
                )

    await handle(error=error, log_chat_id=log_chat_id, bot=bot)


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot):
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error.exception.__class__.__name__,
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )
    if not log_chat_id:
        return

    error_text = hd.quote(
        json.dumps(
            error.update.model_dump(exclude_none=True),
            default=str, ensure_ascii=False
        )[:3500]
    )
    exception = hd.quote(str(error.exception))
    await bot.send_message(
        log_chat_id,
        f"Получено исключение {exception}\n"
        f"во время обработки апдейта {error_text}",
    )


def setup(dp, log_chat_id: int):
    dp.errors.register(
        bot_blocked,
        ExceptionTypeFilter(TelegramForbiddenError)
    )
    dp.errors.register(
        partial(handle_base_error, log_chat_id=log_chat_id),
        ExceptionTypeFilter(BaseError)
    )
    # common handler
    dp.errors.register(
        partial(handle, log_chat_id=log_chat_id)
    )
