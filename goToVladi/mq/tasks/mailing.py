from dataclasses import dataclass

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter
from faststream.rabbit.annotations import RabbitBroker

from goToVladi.core.data.db.dao import DaoHolder

router = RabbitRouter()


@dataclass
class MailingMessage:
    text: str
    user_id: int


@router.subscriber("mail-prepare")
@inject
async def send_mail(
        message: str, dao: FromDishka[DaoHolder], broker: RabbitBroker
):
    user_ids = await dao.user.get_all_active()
    for user_id in user_ids:
        message = MailingMessage(
            text=message,
            user_id=user_id
        )
        await broker.publish(message, queue="mailing")
        await broker.publish(message, queue="mailing")


@router.subscriber("mailing")
@inject
async def send_mail(message: MailingMessage, bot: FromDishka[Bot]):
    await bot.send_message(
        chat_id=message.user_id,
        text=message.text,
    )
