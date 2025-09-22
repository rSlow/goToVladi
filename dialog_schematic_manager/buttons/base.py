import warnings
from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel
from typing_extensions import get_original_bases

from bot_schema_parser.markup import MarkupFactoryEnum, MarkupButton, MarkupButtonType


class ApiButton(BaseModel, ABC):
    __button_types__: ClassVar[dict[str, type["ApiButton"]]] = {}

    __type_key__: ClassVar[str]
    __type_annotation__: ClassVar[str]
    __markup_factories__: ClassVar[list[MarkupFactoryEnum]]

    @classmethod
    def get_model_class(cls, type_name: str):
        return cls.__button_types__[type_name]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if not ABC in get_original_bases(cls):
            if not getattr(cls, "__type_key__"):
                raise AttributeError("")  # TODO no __type_key__

            if not getattr(cls, "__type_annotation__"):
                cls.__type_annotation__ = cls.__type_key__
                warnings.warn("")  # TODO warning no __type_annotation__

            if not getattr(cls, "__markup_factories__"):
                raise AttributeError("")  # TODO no __markup_factories__

            if cls.__type_key__ in cls.__button_types__:
                raise TypeError("")  # TODO already registered
            cls.__button_types__[cls.__type_key__] = cls

    @property
    def type_key(self):
        return self.__type_key__

    @property
    def type_annotation(self):
        return self.__type_annotation__

    @property
    def markup_factories(self):
        return self.__markup_factories__

    type_name: str
    text: str

    @classmethod
    def init_from_dict_config(cls, button_config: dict):
        type_name = getattr(button_config, "type_name")
        if type_name is None:
            raise TypeError("")  # TODO no type_name set
        if type_name not in cls.__button_types__:
            raise TypeError("")  # TODO no registered this type_name
        return cls.__button_types__[type_name].model_validate(button_config)

    @abstractmethod
    def as_aiogram_button(
            self, button_class: MarkupButtonType, button_data: str | None = None
    ) -> MarkupButton:
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


class ActionableButton(ApiButton, ABC):
    @abstractmethod
    def action(self) -> None: ...
