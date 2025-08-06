import warnings
from typing import Iterable, cast

from aiogram import Dispatcher, Bot
from aiogram_dialog import Dialog, Window
from aiogram_dialog.setup import collect_dialogs
from aiogram_dialog.widgets.kbd import Keyboard, ListGroup, Group

from .data_builder import BaseDataBuilder
from .handlers import register_schema_handlers
from .schema_manager import BotSchemaManager
from .schematic import WindowSchema, BotSchema, WindowSchemas
from .sender import SendExecutor, default_send_executor
from .types import SCHEMATIC_ATTR_NAME, MANAGER_KEY


def _get_window_buttons(keyboard: Keyboard) -> Iterable[Keyboard]:
    if isinstance(keyboard, (Group, ListGroup)):
        for sub_keyboard in keyboard.buttons:
            yield from _get_window_buttons(sub_keyboard)

    elif isinstance(keyboard, Keyboard):
        yield keyboard


def get_dp_schematic(dp: Dispatcher):
    window_schemas: WindowSchemas = {}
    buttons: list[Keyboard] = []

    for dialog in cast(Iterable[Dialog], collect_dialogs(dp)):
        for window in dialog.windows.values():
            window_schema: WindowSchema | None = getattr(window, SCHEMATIC_ATTR_NAME, None)
            if isinstance(window_schema, WindowSchema):
                if window_schema.state in window_schemas:
                    warnings.warn(
                        f"Window schema for {str(window_schema.state)} has already been parsed."
                    )

                window_schema.parent_dialog = dialog
                window_schemas[window_schema.window.get_state()] = window_schema

            if isinstance(window, Window):
                if window.keyboard:
                    buttons.extend(_get_window_buttons(window.keyboard))

    # for button in buttons:
    #     if isinstance(button, (Start, SwitchTo)):
    #         target_window = window_schemas.get(button.state)
    #         if target_window:
    #             # TODO create target caller
    #             ...

    return BotSchema(
        window_schemas=window_schemas,
        buttons=buttons
    )


def setup_schema(
        dp: Dispatcher,
        bot: Bot,
        data_builder: BaseDataBuilder,
        send_executor: SendExecutor = default_send_executor
):
    bot_schema: BotSchema = get_dp_schematic(dp)
    bot_schema_manager = BotSchemaManager(
        bot=bot,
        bot_schema=bot_schema,
        data_builder=data_builder,
        send_executor=send_executor
    )
    register_schema_handlers(dp, bot_schema_manager)
    dp.workflow_data.update(
        {
            MANAGER_KEY: bot_schema_manager,
        }
    )
