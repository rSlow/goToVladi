from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from goToVladi.bot.middlewares.config import MiddlewareData


class RegionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData) -> Any:
        dao = data["dao"]
        user = data["user"]
        region = await dao.region.get()
        data["region"] = region

        return await handler(event, data)
