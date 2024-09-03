from aiogram.types import BotCommand

START_COMMAND = BotCommand(
    command="start",
    description="начало работы с ботом"
)
HELP_COMMAND = BotCommand(
    command="help",
    description="помощь"
)
ABOUT_COMMAND = BotCommand(
    command="about",
    description="о боте"
)
CANCEL_COMMAND = BotCommand(
    command="cancel",
    description="на главную"
)
