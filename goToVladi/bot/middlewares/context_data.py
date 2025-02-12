from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.entities import DialogUpdateEvent

from goToVladi.api.config.models import ApiConfig
from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.di.jinja import JinjaRenderer
from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.alert import BotAlert
from goToVladi.core.config import BaseConfig
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import UserDao, RegionDao
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
        data["bot_config"] = await dishka.get(BotConfig)
        data["api_config"] = await dishka.get(ApiConfig)
        data["base_config"] = await dishka.get(BaseConfig)
        data["locker"] = await dishka.get(LockFactory)
        data["scheduler"] = await dishka.get(Scheduler)
        data["alert"] = await dishka.get(BotAlert)
        data["bg_manager_factory"] = self.bg_manager_factory
        data["add_message_viewer"] = AdditionalMessageViewer(data["dialog_manager"])
        data["jinja_renderer"] = await dishka.get(JinjaRenderer)

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
