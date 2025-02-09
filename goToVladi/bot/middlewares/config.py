from typing import TypedDict, Any

from adaptix import Retort
from aiogram import types, Bot, Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import DialogManager, BgManagerFactory
from aiogram_dialog.api.entities import Stack, Context
from aiogram_dialog.context.storage import StorageProxy
from dishka import AsyncContainer

from goToVladi.api.config.models import ApiConfig
from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.di.jinja import JinjaRenderer
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.alert import BotAlert
from goToVladi.core.config import BaseConfig
from goToVladi.core.data.db import dto
from goToVladi.core.scheduler.scheduler import Scheduler
from goToVladi.core.utils.lock_factory import LockFactory


class AiogramMiddlewareData(TypedDict, total=False):
    event_from_user: types.User
    event_chat: types.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: types.Update
    event_router: Router


class DialogMiddlewareData(AiogramMiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class MiddlewareData(DialogMiddlewareData, total=False):
    dishka_container: AsyncContainer
    bot_config: BotConfig
    api_config: ApiConfig
    base_config: BaseConfig
    retort: Retort
    locker: LockFactory
    alert: BotAlert

    scheduler: Scheduler

    user: dto.User | None
    region: dto.Region | None

    bg_manager_factory: BgManagerFactory
    add_message_viewer: AdditionalMessageViewer
    jinja_renderer: JinjaRenderer
