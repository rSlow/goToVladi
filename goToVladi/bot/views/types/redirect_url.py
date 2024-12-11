from urllib.parse import quote

from aiogram.types import InlineKeyboardButton, Chat, User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.utils import CB_SEP
from aiogram_dialog.widgets.kbd import Url

from goToVladi.api.config.models import ApiConfig
from goToVladi.core.config.models import WebConfig


class RedirectUrl(Url):
    async def _render_keyboard(self, data: dict, manager: DialogManager) -> RawKeyboard:
        api_config: ApiConfig = manager.middleware_data["api_config"]
        web_config: WebConfig = manager.middleware_data["base_config"].web
        api_root_path = api_config.get_real_root_path(base_root_path=web_config.real_base_url)

        user: User = manager.middleware_data["event_from_user"]
        chat: Chat = manager.middleware_data["event_chat"]
        original_callback_data: str = manager.middleware_data["aiogd_original_callback_data"]  # TODO error on `/update`
        event_data = original_callback_data.split(CB_SEP, maxsplit=1)[1]

        button_url = await self.url.render_text(data, manager)
        redirecting_url = api_root_path + (f"/redirect/?url={quote(button_url, safe='')}"
                                           f"&user_id={user.id}"
                                           f"&chat_id={chat.id}"
                                           f"&data={event_data}:{self.widget_id}")
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    url=redirecting_url
                )
            ]
        ]
