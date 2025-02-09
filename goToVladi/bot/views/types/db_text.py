from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.core.data.db.dao import MessageTextDao


class DBText(Text):
    def __init__(self, text_label: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text_label = text_label

    @inject
    async def _render_text(
            self, data: dict, manager: DialogManager, message_text_dao: FromDishka[MessageTextDao]
    ) -> str:
        text = await message_text_dao.get_by_name(self.text_label)
        if text is None:
            raise ValueError(f"Text '{self.text_label}' not found!")
        return text.value
