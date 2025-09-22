from aiogram.fsm.state import State

from .window_schema import WindowSchema

# def _get_window_buttons(keyboard: Keyboard) -> Iterable[Keyboard]:
#     if isinstance(keyboard, (Group, ListGroup)):
#         for sub_keyboard in keyboard.buttons:
#             yield from _get_window_buttons(sub_keyboard)
#
#     elif isinstance(keyboard, Keyboard):
#         yield keyboard


# class BotSchema(BaseModel):
#     window_schemas: WindowSchemas = Field(default_factory=dict)
#
#     class Config:
#         arbitrary_types_allowed = True
#
#     def get_dialogs_config(self):
#         windows = []
#         for window in self.window_schemas.values():
#             windows.append(
#                 window.model_dump(
#                     mode="json",
#                     include={"state", "alias", "start_data", "dialog_data"}
#                 )
#             )
#         return windows
#
#     def find(self, state: str) -> WindowSchema | None:
#         state_group, state_name = state.split(":", 1)
#         state = State(state=state_name, group_name=state_group)
#         try:
#             return self.window_schemas[state]
#         except KeyError:
#             return None
