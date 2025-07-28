from aiogram_dialog import Window

from .data_param import DataParam
from .__outer import TargetCaller
from .types import WindowT, SCHEMATIC_ATTR_NAME
from .window_schema import WindowSchema


def with_schematic(
        window: WindowT, alias: str,
        start_data: list[DataParam] | None = None, dialog_data: list[DataParam] | None = None,
        target_caller: TargetCaller | None = None
) -> WindowT:
    if not isinstance(window, Window):
        raise TypeError(f"{window} must be a <{WindowT.__bound__.__name__}> type")

    window_schema = WindowSchema(
        alias=alias,
        state=window.get_state(),
        window=window,
        start_data=start_data or [],  # TODO проверить создание объекта
        dialog_data=dialog_data or [],
        # target_caller=target_caller,
    )
    setattr(window, SCHEMATIC_ATTR_NAME, window_schema)

    return window
