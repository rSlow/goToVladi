from typing import Callable, TypeVar, Union

from pydantic import field_serializer, BaseModel

from bot_schema_parser.types import ParamTypes

FactoryReturn = TypeVar("FactoryReturn")
ParamTypeIn = Union[str, int, float, bool]


class DataParamBase(BaseModel):
    param_name: str


class DataParamIn(DataParamBase):
    param_value: str


class DataParamOut(DataParamBase):
    param_alias: str | None = None
    param_type_in: type[ParamTypeIn] = str
    param_type_name: ParamTypes | None = None

    @field_serializer("param_alias")
    def param_alias_serializer(self, param_alias: str | None):
        if param_alias is None:
            return self.param_name
        return param_alias

    @field_serializer("param_type_name")
    def param_type_name_serializer(self, _param_type_name: str | None):
        if self.param_type_in == str:
            return ParamTypes.STRING
        elif self.param_type_in == int:
            return ParamTypes.INTEGER
        elif self.param_type_in == float:
            return ParamTypes.FLOAT
        elif self.param_type_in == bool:
            return ParamTypes.BOOLEAN

        raise TypeError(f"param_type_in={self.param_type_in}")  # TODO


class DataParam(DataParamBase):
    type_factory: Callable[[ParamTypeIn], FactoryReturn] = str
