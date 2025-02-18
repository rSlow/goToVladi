from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.car_rent import CarRentCardSG
from goToVladi.bot.views import buttons
from goToVladi.bot.views.add_message import AdditionalMessageViewer
from goToVladi.bot.views.types import JinjaTemplate
from goToVladi.core.data.db.dao.car_rent import CarRentDao


@inject
async def car_rent_getter(
        car_rent_dao: FromDishka[CarRentDao], dialog_manager: DialogManager,
        add_message_viewer: AdditionalMessageViewer, **__
):
    car_rent_id = dialog_manager.start_data["car_rent_id"]
    car_rent = await car_rent_dao.get(car_rent_id)
    if car_rent.medias:
        await add_message_viewer.send(car_rent.medias)

    return {
        "car_rent": car_rent,
    }


car_rent_dialog = Dialog(
    Window(
        JinjaTemplate("cards/car_rent.jinja2"),
        # Format("<b>{car_rent.name}</b>"),
        # Format(
        #     text="\nРейтинг редакции - {car_rent.rating}",
        #     when=F["car_rent"].rating,
        # ),
        # Format(
        #     text="\nМинимальный возраст для аренды авто - {car_rent.min_age}",
        #     when=F["car_rent"].min_age,
        # ),
        # Format(
        #     text="\nМинимальный стаж вождения - {car_rent.min_experience}",
        #     when=F["car_rent"].min_experience,
        # ),
        # Format(
        #     text="\nЦена автомобиля от {car_rent.min_price}",
        #     when=F["car_rent"].min_price,
        # ),
        # Format(
        #     text="<u>\n\nТелефон:</u> <code>{car_rent.phone}</code>",
        #     when=F["car_rent"].phone
        # ),
        buttons.CANCEL,
        state=CarRentCardSG.state,
        getter=car_rent_getter
    )
)
