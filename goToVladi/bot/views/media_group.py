import logging

from aiogram import types
from aiogram.enums import ContentType
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, ShowMode

from goToVladi.core.data.db import dto

logger = logging.getLogger(__name__)


async def send_additional_media_group(
        medias: list[dto.BaseAttachment], message: types.Message,
        manager: DialogManager
):
    media_builder = MediaGroupBuilder()

    for media in medias:
        match media.content_type:
            case ContentType.PHOTO:
                media_builder.add_photo(media=FSInputFile(path=media.url))
            case ContentType.VIDEO:
                ...
            case _ as unsupported_type:
                logger.error(f"trying to add {unsupported_type} media in "
                             f"additional media group.")

    additional_messages = await message. \
        answer_media_group(media_builder.build())

    manager.dialog_data["additional_messages"] = [
        message.message_id for message in additional_messages
    ]
    manager.show_mode = ShowMode.DELETE_AND_SEND
