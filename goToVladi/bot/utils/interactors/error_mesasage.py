from aiogram import Bot

from goToVladi.bot.config.models import BotConfig


class ErrorMessageInteractor:
    def __init__(self, bot: Bot, config: BotConfig):
        self.bot = bot
        self.config = config

    async def __call__(self, exc: Exception):
        if exc.args:
            await self.bot.send_message(
                chat_id=self.config.log_chat,
                text=exc.args[0]
            )
