import asyncio
import logging

from aiogram import types, Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.utils.message import delete_message
from goToVladi.core.data.db import dto

logger = logging.getLogger(__name__)


async def send_additional_media_group(
        medias: list[dto.BaseAttachment],
        manager: DialogManager
):
    media_builder = MediaGroupBuilder()

    for media in medias:
        try:
            media_builder.add(
                type=media.content_type,
                media=FSInputFile(path=media.url)
            )
        except ValueError as ex:
            logger.error(
                ex.args[0],
                media.content_type
            )

    middleware_data: MiddlewareData = manager.middleware_data
    bot = middleware_data["bot"]
    chat = middleware_data["event_chat"]

    additional_messages = await bot.send_media_group(
        chat_id=chat.id,
        media=media_builder.build()
    )
    manager.dialog_data["additional_messages"] = [
        message.message_id for message in additional_messages
    ]
    # for sending media group before main message
    manager.show_mode = ShowMode.DELETE_AND_SEND


async def delete_additional_messages(
        callback: types.CallbackQuery, __: Button, manager: DialogManager
):
    # TODO сделать мидлу отлова additional_messages
    additional_messages = manager.dialog_data.pop("additional_messages", [])
    if additional_messages:
        middleware_data: MiddlewareData = manager.middleware_data
        bot: Bot = middleware_data["bot"]
        await asyncio.gather(*[
            delete_message(bot, callback.message.chat.id, additional_message)
            for additional_message in additional_messages
        ])
