from pathlib import Path

import pytest
import pytest_asyncio
from adaptix import Retort
from dishka import Provider, Scope, make_async_container

from goToVladi.api import ApiAppConfig
from goToVladi.api.config.parser.main import load_config as load_api_config
from goToVladi.bot.config.models import BotAppConfig
from goToVladi.bot.config.parser.main import load_config as load_bot_config
from goToVladi.core.config import Paths, BaseConfig
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.di import BaseConfigProvider


@pytest_asyncio.fixture(scope="session")
async def dishka(base_config: BaseConfig):
    mock_provider = Provider(scope=Scope.APP)
    container = make_async_container(
        BaseConfigProvider(),
        mock_provider,
        context={
            BaseConfig: base_config
        }
    )
    yield container
    await container.close()


@pytest.fixture(scope="session")
def paths() -> Paths:
    return Paths(Path(__file__).parent.parent)


@pytest.fixture(scope="session")
def retort() -> Retort:
    return get_base_retort()


@pytest.fixture(scope="session")
def config_dct(paths: Paths) -> dict:
    return read_config_yaml(paths)


@pytest.fixture(scope="session")
def base_config(config_dct: dict, retort: Retort, paths: Paths) -> BaseConfig:
    return load_base_config(config_dct, paths, retort)


@pytest.fixture(scope="session")
def bot_config(retort: Retort, paths: Paths) -> BotAppConfig:
    return load_bot_config(paths, retort)


@pytest.fixture(scope="session")
def api_config(retort: Retort, paths: Paths) -> ApiAppConfig:
    return load_api_config(paths, retort)
