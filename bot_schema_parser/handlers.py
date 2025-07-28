from abc import ABC

from aiogram import Dispatcher, types, F
from aiogram.filters.callback_data import CallbackData
from aiogram_dialog import DialogManager
from aiogram_dialog.context.storage import StorageProxy

from .types import LOADER_BUTTON_PREFIX, BUILDER_KEY

DataFactorySep = "⋮"
LOADER_DATA_PREFIX = "\x1F"


class BaseMessageConfigDataFactory(ABC, CallbackData, sep=DataFactorySep, prefix=LOADER_DATA_PREFIX):
    def __init_subclass__(cls, **kwargs) -> None:
        if "prefix" not in kwargs:
            kwargs["prefix"] = cls.__prefix__
        super().__init_subclass__(**kwargs)


class DirectMessageConfigDataFactory(BaseMessageConfigDataFactory):
    state: str
    start_data: list[str] | None = None
    dialog_data: list[str] | None = None


class LoaderMessageConfigDataFactory(BaseMessageConfigDataFactory):
    identifier: str


def register_schema_handlers(
        dp: Dispatcher,
        message_config_data_factory: BaseMessageConfigDataFactory = LoaderMessageConfigDataFactory,
        # TODO
):
    async def _message_schema_handler(
            message: types.Message, **kwargs
    ):
        ...

    async def _callback_schema_handler(
            callback: types.CallbackQuery, callback_data: LoaderMessageConfigDataFactory,
            dialog_manager: DialogManager, aiogd_storage_proxy: StorageProxy, **kwargs
    ):
        data_builder = kwargs.get(BUILDER_KEY)
        button_config = await data_builder.parse_button_data(callback_data)

        schema_manager = kwargs.get("schema_manager")
        await schema_manager.handle_button(button_config)

    dp.message.register(
        _message_schema_handler,
        F.data.startswith(LOADER_BUTTON_PREFIX)
    )

    dp.callback_query.register(
        _callback_schema_handler,
        message_config_data_factory.filter()
    )
