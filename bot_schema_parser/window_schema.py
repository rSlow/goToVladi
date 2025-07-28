from aiogram.fsm.state import State
from aiogram_dialog import Dialog, Window
from pydantic import BaseModel, Field, field_serializer

from .data_param import DataParamOut, DataParam


class WindowSchema(BaseModel):
    state: State
    alias: str
    window: Window
    parent_dialog: Dialog | None = None
    start_data: list[DataParam] = Field(default_factory=list)
    dialog_data: list[DataParam] = Field(default_factory=list)

    # target_caller: TargetCaller | None = None

    class Config:
        arbitrary_types_allowed = True

    @field_serializer("state")
    def state_serializer(self, state: State):
        return state.state

    @field_serializer("start_data", "dialog_data")
    def data_params_serializer(self, data_params: list[DataParam]):  # noqa
        return [
            DataParamOut(**data_param.model_dump()).model_dump(
                include={"param_name", "param_alias", "param_type_name"}
            )
            for data_param in data_params
        ]


