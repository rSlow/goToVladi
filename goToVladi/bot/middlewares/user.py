from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.entities import DialogUpdateEvent

from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import UserDao, RegionDao


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        user_tg = data.get("event_from_user", None)
        if user_tg is None:
            user = None
        else:
            user_dao = await dishka.get(UserDao)
            if isinstance(event, DialogUpdateEvent):
                user = await user_dao.get_by_tg_id(user_tg.id)
            else:
                user = await user_dao.upsert_user(dto.User.from_aiogram(user_tg))
                if user.region is None:  # TODO куда нибудь перенести в нормальное место
                    region_dao = await dishka.get(RegionDao)
                    region = await region_dao.get_by_ilike_name("Владивосток")
                    if region:
                        await user_dao.set_region(user.tg_id, region.id)
                    user = await user_dao.get_by_tg_id(user.tg_id)

        data["user"] = user

        return await handler(event, data)
