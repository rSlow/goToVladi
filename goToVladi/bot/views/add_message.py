import asyncio
import logging

from aiogram import Bot
from aiogram.types import FSInputFile, Chat
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import Context

from goToVladi.bot.utils.exceptions import UnknownContentTypeError
from goToVladi.bot.utils.media_matching import as_aiogram_content_type
from goToVladi.bot.utils.message import delete_message
from goToVladi.core.data.db import dto

logger = logging.getLogger(__name__)

KEY = "additional_messages"


class AdditionalMessageViewer:
    def __init__(self, manager: DialogManager):
        self._manager = manager

    @property
    def _middleware_data(self) -> dict:
        return self._manager.middleware_data

    @property
    def _bot(self) -> Bot:
        return self._middleware_data["bot"]

    @property
    def _chat(self) -> Chat:
        return self._middleware_data["event_chat"]

    @property
    def _context(self) -> Context:
        return self._middleware_data["aiogd_context"]

    @property
    def _message_ids(self) -> list[int]:
        return self._manager.dialog_data.get(KEY, [])

    @_message_ids.setter
    def _message_ids(self, message_ids: list[int]):
        self._manager.dialog_data[KEY] = message_ids

    async def send(self, medias: list[dto.BaseAttachment]):
        media_builder = MediaGroupBuilder()

        for media in medias:
            try:
                media_builder.add(
                    type=as_aiogram_content_type(media.content.content_type),
                    media=FSInputFile(path=media.url)
                )
            except UnknownContentTypeError as ex:
                logger.error(ex)

        messages = await self._bot.send_media_group(
            chat_id=self._chat.id,
            media=media_builder.build()
        )
        self._message_ids = [message.message_id for message in messages]
        # for sending media group before main message
        self._manager.show_mode = ShowMode.DELETE_AND_SEND

    async def _pop_messages(self):
        return self._manager.dialog_data.pop(KEY, [])

    async def delete(self):
        messages = await self._pop_messages()
        if messages:
            await asyncio.gather(*[
                delete_message(self._bot, self._chat.id, message)
                for message in messages
            ])
