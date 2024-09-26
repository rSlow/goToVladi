import logging

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition, OnPageChangedVariants
from aiogram_dialog.widgets.text import ScrollingText, Text

logger = logging.getLogger(__name__)


class ScrollingSplitText(ScrollingText):
    def __init__(
            self, text: Text, id_: str, page_size: int = 500,
            sep: str = "\n",
            when: WhenCondition = None,
            on_page_changed: OnPageChangedVariants = None,

    ):
        super().__init__(
            text=text, id=id_, page_size=page_size, when=when,
            on_page_changed=on_page_changed
        )
        self.splitter = sep

    def _get_page_table(self, text: str):
        return PageTable(
            text=text, page_size=self.page_size, splitter=self.splitter
        )

    def _get_page_count(self, text: str):
        page_table = self._get_page_table(text)
        return page_table.page_count

    async def _render_text(self, data, manager: DialogManager) -> str:
        text = await self._render_contents(data, manager)
        page_table = self._get_page_table(text)

        page = await self.get_page(manager) + 1
        last_page = page_table.page_count
        current_page = min(last_page, page)

        return page_table.get_page(current_page)

    async def get_page_count(self, data: dict, manager: DialogManager) -> int:
        text = await self._render_contents(data, manager)
        return self._get_page_count(text)


class PageTable:
    def __init__(self, text: str, page_size: int, splitter: str) -> None:
        self.text = text
        self.page_size = page_size
        self.splitter = splitter
        self.pages = self._get_pages()

    def _get_pages(self):
        strings = self.text.split(self.splitter)
        pages = []

        while strings:
            if len(strings[0]) > self.page_size:
                # if len of string more than page_size - splitting it by length.
                string = strings.pop(0)
                for j in range(0, len(string), self.page_size):
                    pages.append(string[j:j + self.page_size])
            else:
                page_len = 0
                page_list = []
                while strings and page_len + len(strings[0]) < self.page_size:
                    string = strings.pop(0)
                    page_list.append(string)
                    page_len += len(string) + len(self.splitter)
                pages.append(self.splitter.join(page_list))

        return pages

    @property
    def page_count(self) -> int:
        return len(self.pages)

    def get_page(self, page_num: int) -> str:
        page_index = min(page_num, self.page_count) - 1
        return self.pages[page_index]
