from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.sea_recreation import SeaRecreationCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.core.data.db.dao import SeaRecreationDao


@inject
async def sea_recreation_getter(
        dialog_manager: DialogManager, add_message_viewer: AdditionalMessageViewer,
        sea_recreation_dao: FromDishka[SeaRecreationDao], **__
):
    sea_recreation_id = dialog_manager.start_data["sea_recreation_id"]
    sea_recreation = await sea_recreation_dao.get(sea_recreation_id)
    if sea_recreation.medias:
        await add_message_viewer.send(sea_recreation.medias)

    return {
        "sea_recreation": sea_recreation
    }


sea_recreation_card_dialog = Dialog(
    Window(
        Format("<b>{sea_recreation.category.name} {sea_recreation.name}</b>"),
        Format(
            "<u>Оценка</u>: {restaurant.rating} / 5 ⭐️",
            when=F["sea_recreation"].rating,
        ),
        Format(
            text="\n{sea_recreation.description}",
            when=F["sea_recreation"].description,
        ),
        Format(
            text="<u>\nТелефон:</u> <code>{sea_recreation.phone}</code>",
            when=F["sea_recreation"].phone
        ),
        buttons.CANCEL,
        getter=sea_recreation_getter,
        state=SeaRecreationCardSG.state,
    )
)
