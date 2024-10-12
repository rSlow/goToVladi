from dataclasses import dataclass

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitExchange
from faststream.rabbit.annotations import RabbitBroker, RabbitMessage

from goToVladi.core.data.db.dao import DaoHolder

router = RabbitRouter()
mail_exchange = RabbitExchange('mail')


@dataclass
class MailingMessage:
    text: str
    user_id: int


@router.subscriber("all", mail_exchange)
@inject
async def send_mail(
        message_text: str, broker: RabbitBroker, dao: FromDishka[DaoHolder]
):
    user_ids = await dao.user.get_all_active()
    for user_id in user_ids:
        message = MailingMessage(
            text=message_text,
            user_id=user_id
        )
        await broker.publish(message, queue="user", exchange=mail_exchange)


@router.subscriber("user", mail_exchange, no_ack=True)
@inject
async def send_mail(
        data: MailingMessage, bot: FromDishka[Bot], message: RabbitMessage
):
    await bot.send_message(
        chat_id=data.user_id,
        text=data.text,
    )
    await message.ack()