import logging

from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import DeliveryCardSG
from goToVladi.bot.utils.dialog import get_social_urls
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.types.redirect_url import RedirectUrl
from goToVladi.core.data.db.dao import DeliveryDao

DESCRIPTION_SCROLL = "description_scroll"

logger = logging.getLogger(__name__)


@inject
async def get_delivery(
        dao: FromDishka[DeliveryDao], dialog_manager: DialogManager,
        add_message_viewer: AdditionalMessageViewer, **__):
    delivery_id = dialog_manager.start_data["delivery_id"]
    delivery = await dao.get(delivery_id)
    if delivery.medias:
        await add_message_viewer.send(delivery.medias)

    return {"delivery": delivery}


delivery_card_dialog = Dialog(
    Window(
        Format("<b>{delivery.name}</b>\n"),
        Format("<u>Оценка</u>: {delivery.rating} / 5 ⭐️"),
        Format("{delivery.description}"),
        Format(
            text="<u>\nТелефон:</u> <code>{delivery.phone}</code>",
            when=F["delivery"].phone
        ),

        Group(
            RedirectUrl(
                text=Const("Сайт 🌐"),
                url=Format("{delivery.site_url}"),
                id="site_url",
                when=F["delivery"].site_url
            ),
            *get_social_urls(data_field_name="delivery"),
            width=2,
            when=F["delivery"]
        ),
        buttons.CANCEL,
        state=DeliveryCardSG.state,
        getter=get_delivery,
    )
)
