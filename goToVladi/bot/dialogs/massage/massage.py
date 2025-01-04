from aiogram import F
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Url, Group
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.massage import MassageCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.core.data.db.dao import MassageDao


@inject
async def massage_getter(
        dialog_manager: DialogManager, add_message_viewer: AdditionalMessageViewer,
        massage_dao: FromDishka[MassageDao], **__
):
    massage_id = dialog_manager.start_data["massage_id"]
    massage = await massage_dao.get(massage_id)
    if massage.medias:
        await add_message_viewer.send(massage.medias)

    return {"massage": massage}


massage_card_dialog = Dialog(
    Window(
        Format("<b>{massage.name}</b>\n"),
        Format(
            text="Минимальная цена - {massage.min_price}\n",
            when=F["massage"].min_price,
        ),
        Format(
            text="{massage.description}",
            when=F["massage"].description,
        ),
        Format(
            text="<u>\nТелефон:</u> <code>{massage.phone}</code>",
            when=F["massage"].phone
        ),

        Group(
            Url(
                text=Const("Сайт 🌐"),
                url=Format("{massage.site_url}"),
                id="site_url",
                when=F["massage"].site_url
            ),
            width=2,
        ),
        buttons.CANCEL,
        getter=massage_getter,
        state=MassageCardSG.state,
    )
)
