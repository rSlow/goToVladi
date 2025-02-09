from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.massage import MassageCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.core.data.db.dao import BarDao


@inject
async def bar_getter(
        dialog_manager: DialogManager, add_message_viewer: AdditionalMessageViewer,
        bar_dao: FromDishka[BarDao], **__
):
    bar_id = dialog_manager.start_data["bar_id"]
    bar = await bar_dao.get(bar_id)
    if bar.medias:
        await add_message_viewer.send(bar.medias)

    return {"bar": bar}


bar_card_dialog = Dialog(
    Window(
        Format("<b>{bar.name}</b>"),
        Format(
            "<u>Оценка</u>: {restaurant.rating} / 5 ⭐️",
            when=F["bar"].rating
        ),
        Format(
            "<u>Средний чек</u>: {restaurant.average_check} ₽",
            when=F["bar"].average_check,
        ),
        Format(
            text="\n{bar.description}",
            when=F["bar"].description,
        ),
        Format(
            text="<u>\nТелефон:</u> <code>{bar.phone}</code>",
            when=F["bar"].phone
        ),
        buttons.CANCEL,
        getter=bar_getter,
        state=MassageCardSG.state,
    )
)
