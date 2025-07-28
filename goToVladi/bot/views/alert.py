from aiogram import Bot


class BotAlert:
    def __init__(self, bot: Bot, log_chat_id: int):
        self.bot = bot
        self.log_chat_id = log_chat_id
        self._bot_name: str | None = None

    async def alert(self, text: str):
        if self._bot_name is None:
            self._bot_name = (await self.bot.get_my_name()).name
        alert_message = f"Error in bot {self._bot_name}:\n----------\n{text}"
        await self.bot.send_message(self.log_chat_id, alert_message)

    __call__ = alert
