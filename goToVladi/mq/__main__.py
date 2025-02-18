import asyncio

from dishka import make_async_container
from dishka.integrations.faststream import (
    setup_dishka as setup_dishka_faststream,
    FastStreamProvider
)
from faststream import FastStream

from goToVladi.bot.config.models import BotAppConfig
from goToVladi.bot.config.parser.main import load_config as load_bot_config
from goToVladi.bot.di import get_bot_providers
from goToVladi.core.config import setup_logging, BaseConfig
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.di import get_common_providers
from goToVladi.core.factory.mq import create_broker
from goToVladi.mq import tasks
from goToVladi.mq.config.models.main import MQAppConfig
from goToVladi.mq.config.parser.main import load_config as load_mq_config
from goToVladi.mq.di.context import FastStreamInjectContext
from goToVladi.mq.utils import middlewares


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    mq_config = load_mq_config(paths, retort)
    bot_config = load_bot_config(paths, retort)

    rabbit_broker = create_broker(mq_config)
    mq_app = FastStream(rabbit_broker)

    di_container = make_async_container(
        *get_common_providers(),
        *get_bot_providers(),
        FastStreamProvider(),
        context={
            BaseConfig: mq_config.as_base(),
            MQAppConfig: mq_config,
            BotAppConfig: bot_config
        }
    )
    setup_dishka_faststream(di_container, mq_app)
    FastStreamInjectContext.container = di_container  # for exception handlers

    tasks.setup(rabbit_broker)
    middlewares.setup(rabbit_broker)

    return mq_app


async def run():
    mq_app = main()
    await mq_app.run()


if __name__ == '__main__':
    asyncio.run(run())
