import logging

from aiogram.exceptions import TelegramForbiddenError
from dishka import FromDishka
from faststream import ExceptionMiddleware

from goToVladi.core.data.db.dao import UserDao
from goToVladi.mq.di.context import FastStreamInjectContext

exc_middleware = ExceptionMiddleware()

logger = logging.getLogger(__name__)


@exc_middleware.add_handler(TelegramForbiddenError)
@FastStreamInjectContext.inject
async def tg_user_blocked(exc: TelegramForbiddenError, dao: FromDishka[UserDao]):
    user_id = exc.method.chat_id
    await dao.deactivate(user_id)
    logger.info("Deactivated user with id %s", user_id)
