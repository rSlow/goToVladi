from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from goToVladi.bot.middlewares.config import MiddlewareData


def is_superuser(data: dict, _: Whenable, __: DialogManager):
    middleware_data: MiddlewareData = data["middleware_data"]
    user = middleware_data["user"]
    superusers = middleware_data["bot_config"].superusers
    return user.tg_id in superusers
