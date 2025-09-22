import warnings
from typing import Iterable, cast

from aiogram import Dispatcher
from aiogram_dialog import Dialog
from aiogram_dialog.setup import collect_dialogs

from .attrs import WINDOW_SCHEMA_KEY
from .types import DialogSchematic
from .window_schema import WindowSchema


def get_dialog_schematic(dp: Dispatcher) -> DialogSchematic:
    dialog_schematic = {}
    # buttons: list[Keyboard] = []

    for dialog in cast(Iterable[Dialog], collect_dialogs(dp)):
        for window in dialog.windows.values():
            window_schema: WindowSchema | None = getattr(window, WINDOW_SCHEMA_KEY, None)
            if isinstance(window_schema, WindowSchema):
                if window_schema.state in dialog_schematic.keys():
                    warnings.warn(
                        f"Window schema for {str(window_schema.state)} has already been parsed."
                    )

                window_schema.parent_dialog = dialog
                dialog_schematic[window_schema.window.get_state()] = window_schema

            # if isinstance(window, Window):
            #     if window.keyboard:
            #         buttons.extend(_get_window_buttons(window.keyboard))

    return dialog_schematic
