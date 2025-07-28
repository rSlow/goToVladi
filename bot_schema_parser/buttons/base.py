import warnings
from abc import ABC, abstractmethod
from typing import ClassVar, Any

from aiogram.types import KeyboardButton
from pydantic import BaseModel
from typing_extensions import get_original_bases

from bot_schema_parser.buttons.types import AiogramButton, AiogramButtonType


class ApiButton(BaseModel, ABC):
    __button_types__: ClassVar[dict[str, type["ApiButton"]]] = {}

    __type_key__: ClassVar[str]
    __type_annotation__: ClassVar[str]

    @classmethod
    def get_model_class(cls, type_name: str):
        return cls.__button_types__[type_name]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if not ABC in get_original_bases(cls):
            if not cls.__type_key__:
                raise AttributeError("")  # TODO no key
            if cls.__type_key__ in cls.__button_types__:
                raise TypeError("")  # TODO already registered
            cls.__button_types__[cls.__type_key__] = cls

            if getattr(cls, "type_annotation") is None:
                cls.__type_annotation__ = cls.__type_key__
                warnings.warn("")  # TODO warning type_key

    @property
    def type_key(self):
        return self.__type_key__

    @property
    def type_annotation(self):
        return self.__type_annotation__

    type_name: str
    text: str

    @classmethod
    @abstractmethod
    def as_aiogram_button(cls, data: Any, button_class: AiogramButtonType) -> AiogramButton:
        ...


class BuildingButton(ApiButton, ABC):
    pass

    # type_prefixes: ClassVar[list[str]] = []  # TODO

    # build_type_prefix: str

    # @classmethod
    # def __pydantic_init_subclass__(cls, **kwargs):
    #     super().__pydantic_init_subclass__(**kwargs)
    #     if cls.build_type_prefix in cls.type_prefixes:
    #         raise TypeError("")  # TODO already registered
    #     cls.type_prefixes.append(cls.build_type_prefix)

    # @classmethod
    # @abstractmethod
    # def get_button_kwargs(cls, data: str) -> dict: ...


class RawButton(ApiButton, ABC):
    pass
