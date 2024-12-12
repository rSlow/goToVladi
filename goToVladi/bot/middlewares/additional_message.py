from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from goToVladi.bot.middlewares.config import MiddlewareData


class AdditionalMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData
    ) -> Any:
        viewer = data.get("add_message_viewer")
        if viewer:
            await viewer.delete()
        return await handler(event, data)
