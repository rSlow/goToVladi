from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.massage import MassageCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.core.data.db.dao import BreakfastDao


@inject
async def breakfast_getter(
        dialog_manager: DialogManager, add_message_viewer: AdditionalMessageViewer,
        breakfast_dao: FromDishka[BreakfastDao], **__
):
    breakfast_id = dialog_manager.start_data["breakfast_id"]
    breakfast = await breakfast_dao.get(breakfast_id)
    if breakfast.medias:
        await add_message_viewer.send(breakfast.medias)

    return {"breakfast": breakfast}


breakfast_card_dialog = Dialog(
    Window(
        Format("<b>{breakfast.name}</b>"),
        Format(
            "<u>Оценка</u>: {restaurant.rating} / 5 ⭐️",
            when=F["breakfast"].rating
        ),
        Format(
            "<u>Средний чек</u>: {restaurant.average_check} ₽",
            when=F["breakfast"].average_check,
        ),
        Format(
            text="\n{breakfast.description}",
            when=F["breakfast"].description,
        ),
        Format(
            text="<u>\nТелефон:</u> <code>{breakfast.phone}</code>",
            when=F["breakfast"].phone
        ),
        buttons.CANCEL,
        getter=breakfast_getter,
        state=MassageCardSG.state,
    )
)
