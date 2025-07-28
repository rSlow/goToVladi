from aiogram import F
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const, Format


def get_social_urls(data_field_name: str):
    F_Item = F[data_field_name]  # noqa
    return [
        Url(
            text=Const("WhatsApp"),
            url=Format(f"{{{data_field_name}.whatsapp}}"),
            id="whatsapp",
            when=F_Item.whatsapp
        ),
        Url(
            text=Const("Instagram"),
            url=Format(f"{{{data_field_name}.instagram}}"),
            id="instagram",
            when=F_Item.instagram
        ),
        Url(
            text=Const("VK"),
            url=Format(f"{{{data_field_name}.vk}}"),
            id="vk",
            when=F_Item.vk
        ),
        Url(
            text=Const("Telegram"),
            url=Format(f"{{{data_field_name}.telegram}}"),
            id="telegram",
            when=F_Item.telegram
        )
    ]


async def update_window(
        dialog_manager: DialogManager, show_mode: ShowMode = ShowMode.DELETE_AND_SEND,
        data: dict = None
):
    if data is None:
        data = {}
    await dialog_manager.update(data, show_mode=show_mode)
