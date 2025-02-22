from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.kbd import ScrollingGroup as BaseScrollingGroup


class ScrollingGroup(BaseScrollingGroup):
    async def _render_pager(self, pages: int, manager: DialogManager) -> RawKeyboard:
        pager = await super()._render_pager(pages, manager)
        pager[0] = pager[0][1:-1]
        return pager
