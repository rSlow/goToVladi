from aiogram import F
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const, Format


def get_social_urls(data_field_name: str):
    return [
        Url(
            text=Const("WhatsApp"),
            url=Format(f"{{{data_field_name}.whatsapp}}"),
            id="whatsapp",
            when=F[data_field_name].whatsapp
        ),
        Url(
            text=Const("Instagram"),
            url=Format(f"{{{data_field_name}.instagram}}"),
            id="instagram",
            when=F[data_field_name].instagram
        ),
        Url(
            text=Const("VK"),
            url=Format(f"{{{data_field_name}.vk}}"),
            id="vk",
            when=F[data_field_name].vk
        ),
        Url(
            text=Const("Telegram"),
            url=Format(f"{{{data_field_name}.telegram}}"),
            id="telegram",
            when=F[data_field_name].telegram
        )
    ]
