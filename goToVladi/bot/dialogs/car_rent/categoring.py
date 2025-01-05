from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from goToVladi.bot.states.car_rent import CarRentSG, CarRentCardSG
from goToVladi.bot.views import buttons
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao.car_rent import CarRentDao


@inject
async def car_classes_getter(car_rent_dao: FromDishka[CarRentDao], user: dto.User, **__):
    region = user.region
    car_classes = await car_rent_dao.get_all_car_classes(region.id_)
    return {
        "region": region,
        "car_classes": car_classes
    }


async def on_car_class_click(_, __, manager: DialogManager, car_class_id: str):
    manager.dialog_data["car_class_id"] = int(car_class_id)
    await manager.next()


car_classes_window = Window(
    Format(
        "Аренда автомобилей в <b>{region.name}</b>.\n"
        "Выберите желаемый класс автомобиля:",
        when=F["car_classes"]
    ),
    Format(
        "К сожалению, в <b>{region.name}</b> мы еще не нашли для Вас лучшие автопрокаты. "
        "Скоро найдем и обязательно добавим!",
        when=~F["car_classes"]
    ),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            id="car_classes",
            items="car_classes",
            item_id_getter=dto.id_getter,
            on_click=on_car_class_click
        ),
        id="car_classes_scroll",
        width=2,
        height=5,
        hide_on_single_page=True,
    ),
    buttons.CANCEL,
    state=CarRentSG.car_class,
    getter=car_classes_getter
)


@inject
async def car_rent_list_getter(
        dialog_manager: DialogManager, user: dto.User, car_rent_dao: FromDishka[CarRentDao], **__
):
    region = user.region
    car_class_id = dialog_manager.dialog_data["car_class_id"]
    car_class = await car_rent_dao.get_car_class(car_class_id)
    car_rents = await car_rent_dao.get_all_rents_in_class(car_class_id, region.id_)
    return {
        "region": region,
        "car_class": car_class,
        "car_rents": car_rents,
    }


async def on_car_rent_click(_, __, manager: DialogManager, car_rent_id: str):
    await manager.start(CarRentCardSG.state, data={"car_rent_id": int(car_rent_id)})


car_rent_list_window = Window(
    Format("Автопрокаты класса \"{car_class.name}\" в {region.name}:"),
    ScrollingGroup(
        Select(
            text=Format("{item.name}"),
            id="car_rents",
            items="car_rents",
            item_id_getter=dto.id_getter,
            on_click=on_car_rent_click
        ),
        id="car_rents_scroll",
        width=1,
        height=5,
        hide_on_single_page=True,
    ),
    buttons.BACK,
    state=CarRentSG.rent_list,
    getter=car_rent_list_getter
)

car_rent_category_dialog = Dialog(
    car_classes_window,
    car_rent_list_window,
)
