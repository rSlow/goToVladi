from __future__ import annotations

from dataclasses import dataclass

from aiogram.client.session.aiohttp import AiohttpSession

from .bot_api import BotApiConfig
from .webhook import WebhookConfig


@dataclass
class BotConfig:
    token: str
    log_chat: int
    """tech chat for tech logs"""
    superusers: list[int]
    bot_api_config: BotApiConfig
    webhook: WebhookConfig | None = None

    def create_session(self) -> AiohttpSession | None:
        if self.bot_api_config.is_local:
            return AiohttpSession(api=self.bot_api_config.create_server())
        return None
