from aiogram import Dispatcher, types, F
from aiogram_dialog import DialogManager
from aiogram_dialog.context.storage import StorageProxy

from bot_schema_parser.button_manager import BotButtonManager
from bot_schema_parser.data_factory import BaseMessageConfigDataFactory

DataFactorySep = "⋮"
LOADER_DATA_PREFIX = "\x1F"


def register_switch_state_handlers(
        dp: Dispatcher,
        bot_button_manager: BotButtonManager,
        # TODO
):
    data_builder = bot_button_manager._data_builder

    async def _message_switch_state_handler(
            message: types.Message, **kwargs
    ):
        ...

    async def _callback_switch_state_handler(
            callback: types.CallbackQuery, callback_data: BaseMessageConfigDataFactory,
            dialog_manager: DialogManager, aiogd_storage_proxy: StorageProxy, **kwargs
    ):
        button_config = await data_builder.parse_data(callback_data)
        await bot_button_manager.handle_button(button_config)

    dp.message.register(
        _message_switch_state_handler,
        F.data.startswith(LOADER_DATA_PREFIX)  # TODO
    )

    dp.callback_query.register(
        _callback_switch_state_handler,
        data_builder.data_factory.filter()
    )
