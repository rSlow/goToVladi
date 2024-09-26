from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager, DialogProtocol
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.common import OnPageChangedVariants
from aiogram_dialog.widgets.kbd import StubScroll
from aiogram_dialog.widgets.kbd.stub_scroll import PagesGetter
from magic_filter import MagicFilter


class PaginationRow(StubScroll):
    def __init__(
            self, id_: str,
            pages: str | int | PagesGetter | MagicFilter,
            on_page_changed: OnPageChangedVariants = None
    ):
        super().__init__(
            id=id_, pages=pages, on_page_changed=on_page_changed
        )

    async def _process_item_callback(
            self, callback: types.CallbackQuery,
            data: str, dialog: DialogProtocol, manager: DialogManager,
    ) -> bool:
        await self.set_page(callback, int(data), manager)
        return True

    async def _render_keyboard(
            self,
            data: dict,
            manager: DialogManager,
    ) -> RawKeyboard:
        return [[
            InlineKeyboardButton(
                text="<",
                callback_data=self._item_callback_data(prev_page),
            ),
            InlineKeyboardButton(
                text=str(current_page + 1),
                callback_data=self._item_callback_data(current_page),
            ),
            InlineKeyboardButton(
                text=">",
                callback_data=self._item_callback_data(next_page),
            ),

        ]]
