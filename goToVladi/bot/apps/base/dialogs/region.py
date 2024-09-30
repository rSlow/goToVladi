from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Select
from aiogram_dialog.widgets.text import Format, Case, Const

from goToVladi.bot.apps.base.states import RegionSG
from goToVladi.bot.utils import buttons
from goToVladi.core.data.db.dao import DaoHolder


async def regions_getter(dao: DaoHolder, **__):
    regions = dao.regions.get_all()
    return {"regions": regions}


start_window = Window(
    Format(
        text="Установлен регион <u><b>{region.name}</b></u>",
        when=F["region"]
    ),
    Format(
        text="Регион поиска не установлен. Нажмите кнопку 'Установить регион'.",
        when=~F["region"]
    ),
    SwitchTo(
        id="set_region",
        text=Case(
            texts={
                True: Const("Сменить регион"),
                ...: Const("Установить регион"),  # default value
            },
            selector=F["region"]
        ),
        state=RegionSG.set
    ),
    # Select(
    #     text=Format("{region.name}"),
    #     id="regions",
    #     items="regions",
    #     item_id_getter=dto.id_getter,
    #     when=~F["region"]
    # ),
    buttons.CANCEL,
    state=RegionSG.start
)

set_region_window = Window(
    Select(),
    buttons.BACK,
    state=RegionSG.set
)

region_dialog = Dialog(
    start_window,
)
