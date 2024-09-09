from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog import StartMode
from dishka import FromDishka
from jinja2 import Environment

from goToVladi.bot.apps.base.states import MainMenuSG
from goToVladi.bot.views import commands
from goToVladi.bot.views.jinja import render_template


async def cmd_start(_: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=MainMenuSG.state, mode=StartMode.RESET_STACK
    )


async def cmd_help(
        message: types.Message, dialog_manager: DialogManager,
        jinja: FromDishka[Environment]
):
    template = jinja.get_template("help.jinja2")
    await message.answer(render_template(template))
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_about(message: types.Message, dialog_manager: DialogManager):
    await message.answer(f"Разработчик бота - @rs1ow\n"
                         f"Дизайнер бота - @petrunin_artem")
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


def setup():
    router = Router(name=__name__)
    router.message.register(cmd_start, Command(commands.START_COMMAND))
    router.message.register(cmd_help, Command(commands.HELP_COMMAND))
    router.message.register(cmd_about, Command(commands.ABOUT_COMMAND))

    return router
