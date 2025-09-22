from abc import ABC, abstractmethod

from aiogram import Dispatcher
from aiogram_dialog.widgets.kbd import Keyboard, Button, Select, Counter, ListGroup, SwitchPage, \
    NumberedPager, ScrollingGroup
from aiogram_dialog.widgets.kbd.checkbox import BaseCheckbox


class TargetCaller(ABC):
    @abstractmethod
    def create_button(self): ...

    @abstractmethod
    def parse_event(self): ...


class ButtonCaller(TargetCaller):
    def create_button(self): ...

    def parse_event(self): ...


def parse_target_button(button: Keyboard):
    if isinstance(button, Button):
        ...
    if isinstance(button, Select):
        "item_id"
    if isinstance(button, BaseCheckbox):
        "checked"
    if isinstance(button, Counter):
        "-" or "" or "+"  # noqa
    if isinstance(button, ListGroup):
        "{item_id}:{btn.callback_data}"
    if isinstance(button, (SwitchPage, NumberedPager)):
        "target_page"
    if isinstance(button, ScrollingGroup):
        "{target_page - 1}"

    raise TypeError


def register_dialog_schema_handlers(dp: Dispatcher):
    ...

# def get_target_buttons(schema: WindowSchema):
#     buttons = []
#     keyboard = schema.window.keyboard
#     if isinstance(keyboard, Group):
#         for button in keyboard.buttons:
#             ...
#
#     return buttons
#
# class WindowSchematicFactory:
#     def __init__(self, dp: Dispatcher):
#         self.dp = dp
#         self.window: WindowT | None = None
#
#     def __call__(self, window: WindowT, alias: str) -> WindowT:
#         ...
#
#     def with_start_data(self, data: StartData):
#         self._check_window_exist()
#         ...
#
#     def with_dialog_data(self):
#         self._check_window_exist()
#         ...
#
#     def _check_window_exist(self):
#         if not isinstance(self.window, Window):
#             raise
#         return True
#


# if target_window.parent_dialog is current_window.parent_dialog:
#     await bg.update({})
#     await bg.switch_to(target_window.state)
# else:
#     await bg.start(target_window.state, data={})
