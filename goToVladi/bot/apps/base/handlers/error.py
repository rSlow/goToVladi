import json
import logging
import typing
from functools import partial

from aiogram import Dispatcher, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, NoContextError

from goToVladi.bot.apps.base.states import MainMenuSG
from goToVladi.core.utils.exceptions.base import BaseError

logger = logging.getLogger(__name__)


async def handle_sh_error(error: ErrorEvent, log_chat_id: int, bot: Bot):
    exception: BaseError = typing.cast(BaseError, error.exception)
    if callback := error.update.callback_query:
        await callback.answer(exception.notify_user, show_alert=True)
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


async def clear_unknown_intent(error: ErrorEvent, bot: Bot):
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


async def no_context(error: ErrorEvent, bot: Bot,
                     dialog_manager: DialogManager):
    logger.exception(
        "No dialog context found",
        error.exception.__class__.__name__,
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )
    message = error.update.message or error.update.callback_query.message
    if message:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Произошла ошибка бота, мы вынуждены вернуть вас "
                 f"в главное меню, и уже работаем над устранением 🛠"
        )
        await dialog_manager.start(
            MainMenuSG.main_state, mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND
        )


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
        f"во время обработки апдейта "
        f"{error_text}\n",
    )


def setup(dp: Dispatcher, log_chat_id: int):
    dp.errors.register(
        partial(handle_sh_error, log_chat_id=log_chat_id),
        ExceptionTypeFilter(BaseError)
    )
    dp.errors.register(
        clear_unknown_intent,
        ExceptionTypeFilter(UnknownIntent)
    )
    dp.errors.register(
        no_context,
        ExceptionTypeFilter(NoContextError)
    )
    dp.errors.register(
        partial(handle, log_chat_id=log_chat_id)
    )
