from aiogram import types, Bot
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.di.jinja import JinjaRenderer
from goToVladi.bot.states.cooperation import CooperationSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.types import JinjaTemplate
from goToVladi.core.config.models import AppConfig
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao.cooperation import CooperationDao


@inject
async def on_text_input(
        message: types.Message, _, manager: DialogManager, data: str,
        dao: FromDishka[CooperationDao], bot: FromDishka[Bot], jinja: FromDishka[JinjaRenderer],
        app_config: FromDishka[AppConfig]
):
    user: dto.User = manager.middleware_data["user"]
    await dao.add(text=data, username=user.username)
    await message.answer("Заявка принята, в ближайшее время мы ее рассмотрим!")
    for user_id in app_config.admins:  # TODO fix this
        await bot.send_message(
            chat_id=user_id,
            text=jinja.render_template(
                "cooperation/card.jinja2",
                context={"data": data, "user": user}
            )
        )
    await manager.done()


cooperation_dialog = Dialog(
    Window(
        JinjaTemplate("cooperation/input.jinja2"),
        TextInput(
            id="cooperation_input",
            on_success=on_text_input
        ),
        buttons.CANCEL,
        state=CooperationSG.input
    )
)
