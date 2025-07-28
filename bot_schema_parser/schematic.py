from aiogram.fsm.state import State
from aiogram_dialog.widgets.kbd import Keyboard
from pydantic import BaseModel, Field

from .window_schema import WindowSchema

WindowSchemas = dict[State, WindowSchema]


class BotSchema(BaseModel):
    window_schemas: WindowSchemas = Field(default_factory=dict)
    buttons: list[Keyboard] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def get_dialogs_config(self):
        windows = []
        for window in self.window_schemas.values():
            windows.append(
                window.model_dump(
                    mode="json",
                    include={"state", "alias", "start_data", "dialog_data"}
                )
            )
        return windows

    def find(self, state: str) -> WindowSchema | None:
        state_group, state_name = state.split(":", 1)
        state = State(state=state_name, group_name=state_group)
        try:
            return self.window_schemas[state]
        except KeyError:
            return None
