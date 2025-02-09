from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog import StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from jinja2 import Environment

from goToVladi.bot.states.region import RegionSG
from goToVladi.bot.states.start import MainMenuSG
from goToVladi.bot.views import commands
from goToVladi.bot.views.jinja import render_template
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import EventLogDao
from goToVladi.core.data.db.dao.message_text import MessageTextDao


@inject
async def cmd_start(
        message: types.Message, dialog_manager: DialogManager, user: dto.User,
        event_dao: FromDishka[EventLogDao], message_dao: FromDishka[MessageTextDao],
):
    start_event = await event_dao.get_last_by_user(user.tg_id, "/start")
    if start_event is None:
        greeting_message = await message_dao.get_by_name("greeting")
        if greeting_message:
            await message.answer(text=greeting_message.value)
    await dialog_manager.start(state=MainMenuSG.state, mode=StartMode.RESET_STACK)


@inject
async def cmd_help(
        message: types.Message, dialog_manager: DialogManager,
        jinja: FromDishka[Environment]
):
    template = jinja.get_template("help.jinja2")
    await message.answer(render_template(template))
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_about(message: types.Message, dialog_manager: DialogManager):
    await message.answer(
        f"Разработчик бота - @rs1ow\n"
        f"Дизайнер бота - @petrunin_artem"
    )
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_update(message: types.Message, dialog_manager: DialogManager):
    await message.delete()
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_region(_: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(RegionSG.start)


def setup():
    router = Router(name=__name__)

    router.message.register(cmd_start, Command(commands.START))
    router.message.register(cmd_help, Command(commands.HELP))
    router.message.register(cmd_about, Command(commands.ABOUT))
    router.message.register(cmd_update, Command(commands.UPDATE))
    router.message.register(cmd_region, Command(commands.REGION))

    return router
