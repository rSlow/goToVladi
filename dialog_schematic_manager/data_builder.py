from abc import abstractmethod, ABC
from typing import Any, Generic

from bot_schema_parser.buttons.base import BuildingButton
from bot_schema_parser.data_factory import BaseMessageConfigDataFactory, DF, \
    LoaderMessageConfigDataFactory
from bot_schema_parser.loader import ButtonConfigLoader


class BaseDataBuilder(ABC, Generic[DF]):
    @abstractmethod
    async def create_data(self, button: BuildingButton) -> str: ...

    @abstractmethod
    async def parse_data(self, data: Any) -> BuildingButton: ...

    @abstractmethod
    @property
    def data_factory(self) -> type[BaseMessageConfigDataFactory]: ...


class BaseSwitchDataBuilder(BaseDataBuilder[DF], ABC):
    pass


# class DirectSwitchDataBuilder(BaseSwitchDataBuilder[DirectMessageConfigDataFactory]):
#     async def create_data(self, button: BuildingButton):
#         return self.data_factory(
#             state=...,
#             start_data=...,
#             dialog_data=...,
#         ).pack()
#
#     async def parse_data(self, data: DF) -> BuildingButton:
#         ...
#
#     @property
#     def data_factory(self):
#         return DirectMessageConfigDataFactory


class LoaderSwitchDataBuilder(BaseSwitchDataBuilder[LoaderMessageConfigDataFactory]):
    def __init__(self, config_loader: ButtonConfigLoader):
        self._config_loader = config_loader

    async def create_data(self, button: BuildingButton):
        button_config_identifier = await self._config_loader.save_button_config(button)
        return self.data_factory(
            identifier=str(button_config_identifier)
        ).pack()

    async def parse_data(self, data: DF) -> BuildingButton:
        identifier = self._config_loader.parse_message(data.identifier)
        return await self._config_loader.load_button_config(identifier)

    @property
    def data_factory(self):
        return LoaderMessageConfigDataFactory
