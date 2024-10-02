import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.utils.message import delete_message


class AdditionalMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData
    ) -> Any:
        bot = data["bot"]
        chat = data["event_chat"]
        context = data["aiogd_context"]
        if context:
            messages = context.dialog_data.pop("additional_messages", [])
            await asyncio.gather(*[
                delete_message(bot, chat.id, message)
                for message in messages
            ])

        return await handler(event, data)
