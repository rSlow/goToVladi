import warnings
from typing import Iterable, cast

from aiogram import Dispatcher
from aiogram_dialog import Dialog, Window
from aiogram_dialog.setup import collect_dialogs
from aiogram_dialog.widgets.kbd import Keyboard, SwitchTo, Start, ListGroup, Group

from .data_builder import BaseSwitchDataBuilder
from .handlers import register_schema_handlers
from .schematic import WindowSchema, BotSchema, WindowSchemas
from .types import SCHEMATIC_ATTR_NAME, SCHEMA_KEY, BUILDER_KEY


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

    for button in buttons:
        if isinstance(button, (Start, SwitchTo)):
            target_window = window_schemas.get(button.state)
            if target_window:
                # TODO create target caller
                ...

    return BotSchema(
        window_schemas=window_schemas,
        buttons=buttons
    )


def setup_schema(
        dp: Dispatcher,
        data_builder: BaseSwitchDataBuilder
):
    bot_schema: BotSchema = get_dp_schematic(dp)
    register_schema_handlers(dp, data_builder.data_factory)
    dp.workflow_data.update(
        {
            SCHEMA_KEY: bot_schema,
            BUILDER_KEY: data_builder
        }
    )
