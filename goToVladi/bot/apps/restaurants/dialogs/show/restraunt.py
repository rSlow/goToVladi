import logging

from aiogram import F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll as MScroll
from aiogram_dialog.widgets.kbd import Group, Url
from aiogram_dialog.widgets.text import Const, Format

from goToVladi.bot.apps.restaurants.states import RestaurantSG
from goToVladi.bot.utils import buttons
from goToVladi.bot.utils.scroll import normalize_scroll
from goToVladi.bot.views.media_group import send_additional_media_group
from goToVladi.bot.views.types import PaginationRow
from goToVladi.bot.views.types.scrolls import ScrollingSplitText
from goToVladi.bot.views.types.scrolls.split_text import PageTable
from goToVladi.core.config import BaseConfig
from goToVladi.core.data.db.dao import DaoHolder

PHOTOS_SCROLL = "photos_scroll"
DESCRIPTION_SCROLL = "description_scroll"

logger = logging.getLogger(__name__)


async def get_restaurant(
        dao: DaoHolder, base_config: BaseConfig,
        dialog_manager: DialogManager, **__
):
    restaurant_id = dialog_manager.dialog_data["restaurant_id"]
    restaurant = await dao.restaurant.get(restaurant_id)

    if restaurant.medias:
        await send_additional_media_group(
            medias=restaurant.medias, manager=dialog_manager
        )

    if restaurant.description:
        description_scroll: MScroll = dialog_manager.find(DESCRIPTION_SCROLL)
        await normalize_scroll(
            # TODO снести page_table
            PageTable(restaurant.description, 600, "\n").pages,
            description_scroll
        )

    return {
        "restaurant": restaurant,
        "description_length": len(restaurant.description or "")
    }


restaurant_window = Window(
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
        Url(
            text=Const("Сайт 🌐"),
            url=Format("{restaurant.site_url}"),
            id="site_url",
            when=F["restaurant"].site_url
        ),
        Url(
            text=Const("WhatsApp"),
            url=Format("{restaurant.whatsapp}"),
            id="whatsapp",
            when=F["restaurant"].whatsapp
        ),
        Url(
            text=Const("Instagram"),
            url=Format("{restaurant.instagram}"),
            id="instagram",
            when=F["restaurant"].instagram
        ),
        Url(
            text=Const("VK"),
            url=Format("{restaurant.vk}"),
            id="vk",
            when=F["restaurant"].vk
        ),
        Url(
            text=Const("Telegram"),
            url=Format("{restaurant.telegram}"),
            id="telegram",
            when=F["restaurant"].telegram
        ),
        width=2,
        when=F["restaurant"]  # .paid TODO сделать фильтрацию по оплате
    ),
    buttons.BACK,
    # Back(
    #     text=Const("Назад ◀"),
    #     on_click=delete_additional_messages
    # ),
    state=RestaurantSG.restaurant,
    getter=get_restaurant,
)
