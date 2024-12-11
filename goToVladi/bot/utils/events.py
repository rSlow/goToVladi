from datetime import datetime

import pytz
from aiogram import types as t
from aiogram.enums import ContentType
from aiogram_dialog.utils import CB_SEP

from goToVladi.core.data.db import dto


def from_message(message: t.Message):
    match message.content_type:
        case ContentType.TEXT:
            data = (message.text or "")[:255]
        case ContentType.DOCUMENT:
            data = message.document.file_id
        case ContentType.PHOTO:
            data = message.photo[-1].file_id
        case ContentType.VIDEO:
            data = message.video[-1].file_id
        case ContentType.AUDIO:
            data = message.audio[-1].file_id
        case _ as content_type:
            data = "unexpected content type: " + content_type

    return dto.LogEvent(
        type_="message",
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        content_type=message.content_type,
        dt=message.date,
        data=data
    )


def from_callback_query(callback: t.CallbackQuery):
    dt = datetime.now(tz=pytz.UTC)
    chat_id = callback.message.chat.id
    if isinstance(callback.message, t.InaccessibleMessage):
        return dto.LogEvent(
            type_="inaccessible_callback_query",
            chat_id=chat_id,
            dt=dt
        )
    if callback.data and CB_SEP in callback.data:
        data = callback.data.split(CB_SEP, maxsplit=1)[1]
    else:
        data = callback.data

    return dto.LogEvent(
        type_="callback_query",
        user_id=callback.from_user.id,
        chat_id=chat_id,
        dt=dt,
        data=data
    )
