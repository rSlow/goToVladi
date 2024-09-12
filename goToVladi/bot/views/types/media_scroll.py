from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import OnPageChangedVariants, \
    WhenCondition
from aiogram_dialog.widgets.kbd import StubScroll
from aiogram_dialog.widgets.kbd.stub_scroll import PagesGetter
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Text
from magic_filter import MagicFilter


class MediaScroll(StaticMedia, StubScroll):
    def __init__(
            self,
            id_: str,
            pages: str | int | PagesGetter | MagicFilter,
            on_page_changed: OnPageChangedVariants = None,
            path: Text | str | None = None,
            url: Text | str | None = None,
            type_: ContentType = ContentType.PHOTO,
            use_pipe: bool = False,
            media_params: dict = None,
            when: WhenCondition = None
    ):
        StubScroll.__init__(
            self, id=id_, on_page_changed=on_page_changed, pages=pages
        )
        StaticMedia.__init__(
            self, path=path, url=url, type=type_, use_pipe=use_pipe,
            media_params=media_params, when=when,
        )

    async def get_page_count(self, data: dict, manager: DialogManager) -> int:
        return self._pages(data, self, manager)
