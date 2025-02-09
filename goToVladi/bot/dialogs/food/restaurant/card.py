import logging

from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.food import RestaurantCardSG
from goToVladi.bot.utils.dialog import get_social_urls
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.types import PaginationRow
from goToVladi.bot.views.types.redirect_url import RedirectUrl
from goToVladi.bot.views.types.scrolls import ScrollingSplitText
from goToVladi.core.data.db.dao import RestaurantDao

DESCRIPTION_SCROLL = "description_scroll"

logger = logging.getLogger(__name__)


@inject
async def get_restaurant(
        dao: FromDishka[RestaurantDao], dialog_manager: DialogManager,
        add_message_viewer: AdditionalMessageViewer, **__):
    restaurant_id = dialog_manager.start_data["restaurant_id"]
    restaurant = await dao.get(restaurant_id)
    if restaurant.medias:
        await add_message_viewer.send(restaurant.medias)

    return {
        "restaurant": restaurant,
        "description_length": len(restaurant.description or "")
    }


restaurant_card_dialog = Dialog(
    Window(
        Format("<b>{restaurant.name}</b>\n"),
        Format("<u>Оценка</u>: {restaurant.rating} / 5 ⭐️"),
        Format("<u>Средний чек</u>: {restaurant.average_check} ₽\n"),
        ScrollingSplitText(
            text=Format("{restaurant.description}"),
            id_=DESCRIPTION_SCROLL,
            page_size=600,
            when=F["restaurant"].description,
            sep="\n"
        ),
        Format(
            text="<u>\nТелефон:</u> <code>{restaurant.phone}</code>",
            when=F["restaurant"].phone
        ),

        PaginationRow(
            id_=DESCRIPTION_SCROLL, scroll=DESCRIPTION_SCROLL,
            current_text=Format("Описание {current_page1} / {pages}"),
            when=F["description_length"] >= 600
        ),

        Group(
            RedirectUrl(
                text=Const("Сайт 🌐"),
                url=Format("{restaurant.site_url}"),
                id="site_url",
                when=F["restaurant"].site_url
            ),
            *get_social_urls(data_field_name="restaurant"),
            width=2,
            when=F["restaurant"]  # .paid TODO сделать фильтрацию по оплате
        ),
        buttons.CANCEL,
        state=RestaurantCardSG.state,
        getter=get_restaurant,
    )
)
