from enum import StrEnum, auto

from pydantic import BaseModel

from .data_builder import BaseSwitchDataBuilder, DirectSwitchDataBuilder




class SchemaConfig(BaseModel):
    markup_factory: MarkupFactory = MarkupFactory.INLINE
    data_builder: type[BaseSwitchDataBuilder] = DirectSwitchDataBuilder

    class Config:
        arbitrary_types_allowed = True
