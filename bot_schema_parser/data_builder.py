from abc import abstractmethod, ABC
from typing import TypeVar, Any, Generic

from .buttons.base import BuildingButton
from .handlers import LoaderMessageConfigDataFactory, DirectMessageConfigDataFactory, \
    BaseMessageConfigDataFactory
from .loader import ButtonConfigLoader

DF = TypeVar("DF", bound=BaseMessageConfigDataFactory, covariant=True)


class BaseDataBuilder(ABC, Generic[DF]):
    def __init__(self, data_factory: DF):
        self._data_factory = data_factory

    @abstractmethod
    async def create_data(self, button: BuildingButton) -> str: ...

    @abstractmethod
    async def parse_data(self, data: Any) -> BuildingButton: ...


class BaseSwitchDataBuilder(BaseDataBuilder[DF], ABC):
    pass
    # def __init_subclass__(cls, **kwargs):
    #     cls._data_factory: type[DF] = get_original_bases(cls)[0].__args__[0]
    #     super().__init_subclass__(**kwargs)


class DirectSwitchDataBuilder(BaseSwitchDataBuilder[DirectMessageConfigDataFactory]):
    async def create_data(self, button: BuildingButton):
        return self._data_factory(
            state=...,
            start_data=...,
            dialog_data=...,
        ).pack()

    async def parse_data(self, data: DF) -> BuildingButton:
        ...


class LoaderSwitchDataBuilder(BaseSwitchDataBuilder[LoaderMessageConfigDataFactory]):
    def __init__(self, loader: ButtonConfigLoader):
        self._loader = loader

    async def create_data(self, button: BuildingButton):
        button_config_identifier = await self._loader.save_button_config(button)
        return self.data_factory(identifier=str(button_config_identifier)).pack()

    async def parse_data(self, data: DF) -> BuildingButton:
        identifier = self._loader.parse_message(data.identifier)
        button_config = await self._loader.load_button_config(identifier)
        return BuildingButton.model_validate(button_config)

    @property
    def data_factory(self):
        return LoaderMessageConfigDataFactory
