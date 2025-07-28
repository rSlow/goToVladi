from abc import abstractmethod
from typing import Protocol, Iterable

from aiogram import Bot

from bot_schema_parser.buttons.types import KeyboardMarkup


class SendExecutor(Protocol):
    @abstractmethod
    async def __call__(
            self,
            bot: Bot,
            chat_ids: Iterable[int],
            text: str,
            markup: KeyboardMarkup
    ) -> None:
        pass


class SimpleSendExecutor(SendExecutor):
    async def __call__(
            self,
            bot: Bot,
            chat_ids: Iterable[int],
            text: str,
            markup: KeyboardMarkup
    ) -> None:
        for chat_id in chat_ids:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup
            )


default_send_executor = SimpleSendExecutor()
