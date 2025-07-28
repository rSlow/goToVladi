import logging

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.utils.interactors.error_mesasage import ErrorMessageInteractor
from goToVladi.core.data.db.dao import MessageTextDao

logger = logging.getLogger(__name__)


class DBText(Text):
    __text_keys = set()

    def __new__(cls, *args, **kwargs):
        cls.__text_keys.add(args[0])
        return super().__new__(cls)

    def __init__(self, text_label: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text_label = text_label

    @inject
    async def _render_text(
            self, data: dict, manager: DialogManager, message_text_dao: FromDishka[MessageTextDao],
            error_message_interactor: FromDishka[ErrorMessageInteractor]
    ) -> str:
        text = await message_text_dao.get_by_name(self.text_label)
        if text is None:
            await error_message_interactor(ValueError(f"Text '{self.text_label}' not found!"))
            return ("Тут должен быть какой то текст, но мы его забыли добавить :) "
                    "Уже знаем об этом и бежим добавлять!")
        return text.value

    @classmethod
    async def check_keys(cls, message_text_dao: MessageTextDao):
        missing_keys = await message_text_dao.get_missing_keys(cls.__text_keys)
        if missing_keys:
            msg = ("\n" + "Database text have missing keys:" + "\n"
                   + "\n".join([f"  -> {key.name}" for key in missing_keys]))
            logger.warning(msg)
        else:
            logger.info("Database text have all needed keys.")
