from typing import Callable, Any, Awaitable

from adaptix import Retort
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.entities import DialogUpdate

from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.core.config import BaseConfig
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.scheduler.scheduler import Scheduler
from goToVladi.core.utils.lock_factory import LockFactory


class ContextDataMiddleware(BaseMiddleware):
    def __init__(self, bg_manager_factory: BgManagerFactory):
        self.bg_manager_factory = bg_manager_factory

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        dao_holder: DaoHolder = await dishka.get(DaoHolder)
        data["bot_config"] = await dishka.get(BotConfig)
        data["base_config"] = await dishka.get(BaseConfig)
        data["retort"] = await dishka.get(Retort)
        data["locker"] = await dishka.get(LockFactory)
        data["scheduler"] = await dishka.get(Scheduler)
        data["dao"] = dao_holder
        data["bg_manager_factory"] = self.bg_manager_factory

        user_tg = data.get("event_from_user", None)
        if user_tg is None:
            user = None
        else:
            if isinstance(event, DialogUpdate):
                user = await dao_holder.user.get_by_tg_id(user_tg.id)
            else:
                user = await dao_holder.user.upsert_user(
                    dto.User.from_aiogram(user_tg)
                )
        data["user"] = user

        return await handler(event, data)
