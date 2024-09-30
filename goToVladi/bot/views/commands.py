from aiogram.types import BotCommand

START = BotCommand(
    command="start",
    description="в начало"
)
HELP = BotCommand(
    command="help",
    description="помощь"
)
ABOUT = BotCommand(
    command="about",
    description="о боте"
)
UPDATE = BotCommand(
    command="update",
    description="обновить"
)
REGION = BotCommand(
    command="region",
    description="выбрать город"
)
