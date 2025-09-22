from abc import ABC
from typing import TypeVar

from aiogram.filters.callback_data import CallbackData

DataFactorySep = "⋮"
LOADER_DATA_PREFIX = "\x1F"


class BaseMessageConfigDataFactory(ABC, CallbackData,
                                   sep=DataFactorySep,
                                   prefix=LOADER_DATA_PREFIX):
    def __init_subclass__(cls, **kwargs) -> None:
        if "prefix" not in kwargs:
            kwargs["prefix"] = getattr(cls, "__prefix__", None)
        super().__init_subclass__(**kwargs)


class DirectMessageConfigDataFactory(BaseMessageConfigDataFactory):
    state: str
    start_data: list[str] | None = None
    dialog_data: list[str] | None = None


class LoaderMessageConfigDataFactory(BaseMessageConfigDataFactory):
    identifier: str


DF = TypeVar("DF", bound=BaseMessageConfigDataFactory, covariant=True)
