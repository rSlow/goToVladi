import logging
import typing as t
from functools import partial

from aiogram import Bot
from aiogram.exceptions import AiogramError
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd
from aiogram_dialog import BgManagerFactory

from goToVladi.bot.utils.exceptions import UserNotifyException
from goToVladi.bot.utils.markdown import get_update_text
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.utils.exceptions.base import BaseError

logger = logging.getLogger(__name__)


def get_chat_id_from_error(error: ErrorEvent) -> int:
    update = error.update
    if update.callback_query:
        return update.callback_query.message.chat.id
    elif update.message:
        return update.message.chat.id
    elif update.business_message:
        return update.business_message.chat.id


def get_user_id_from_error(error: ErrorEvent) -> int:
    update = error.update
    if update.callback_query:
        return update.callback_query.from_user.id
    elif update.message:
        return update.message.from_user.id
    elif update.business_message:
        return update.business_message.from_user.id


async def bot_blocked(error: ErrorEvent, dao: DaoHolder):
    user_id = get_user_id_from_error(error)
    await dao.user.deactivate(user_id)
    logger.info("Деактивирован пользователь с ID %s", user_id)


async def handle_notify_exception(error: ErrorEvent, bot: Bot, dialog_bg_factory: BgManagerFactory):
    exception = t.cast(UserNotifyException, error.exception)
    chat_id = get_chat_id_from_error(error)
    if chat_id is not None:
        await bot.send_message(
            chat_id=chat_id,
            text=exception.message
        )
        user_id = get_user_id_from_error(error)
        if user_id is not None:
            bg = dialog_bg_factory.bg(bot=bot, user_id=user_id, chat_id=chat_id)
            await bg.update({}, show_mode=exception.show_mode)


async def handle_base_error(error: ErrorEvent, log_chat_id: int, bot: Bot):
    exception = t.cast(BaseError, error.exception)
    chat_id = exception.chat_id or exception.user_id
    if chat_id is None:
        chat_id = get_chat_id_from_error(error)

    if c := error.update.callback_query:
        await c.answer(exception.note_for_user, show_alert=True)

    elif chat_id and exception.user_note_template is not None:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=exception.note_for_user
            )
        except AiogramError as ex:
            logger.exception(
                "Ошибка отправки сообщения пользователю:",
                exc_info=ex
            )

    if exception.log:
        await handle(error=error, log_chat_id=log_chat_id, bot=bot)


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot):
    logger.exception(
        "Получено исключение: %s, во время обработки апдейта %s",
        str(error.exception),
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )

    if not log_chat_id:
        return
    await bot.send_message(
        log_chat_id,
        f"Получено исключение {hd.quote(str(error.exception))}\n"
        f"во время обработки апдейта {get_update_text(error.update)}",
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
    dp.errors.register(
        handle_notify_exception,
        ExceptionTypeFilter(UserNotifyException)
    )

    # common handler
    dp.errors.register(
        partial(handle, log_chat_id=log_chat_id)
    )
