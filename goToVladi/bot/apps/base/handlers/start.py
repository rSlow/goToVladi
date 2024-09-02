from aiogram import types
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from jinja2 import Environment

from bot.views.jinja import render_template


@inject
async def start(message: types.Message, jinja: FromDishka[Environment]):
    template = jinja.get_template("start.jinja2")
    await message.answer(render_template(template))
