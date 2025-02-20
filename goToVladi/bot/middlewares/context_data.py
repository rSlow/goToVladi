from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory

from goToVladi.api.config.models import ApiConfig
from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.di.jinja import JinjaRenderer
from goToVladi.bot.middlewares.config import MiddlewareData
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.alert import BotAlert
from goToVladi.core.config import BaseConfig
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

        return await handler(event, data)
