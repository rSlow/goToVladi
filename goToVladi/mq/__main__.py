import asyncio

from dishka import make_async_container
from dishka.integrations.faststream import \
    setup_dishka as setup_dishka_faststream, FastStreamProvider
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from goToVladi.core.config import setup_logging
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.di import get_common_providers
from goToVladi.mq import tasks
from goToVladi.mq.config.models.main import MQAppConfig
from goToVladi.mq.config.parser.main import load_config


def main():
    paths = get_paths()
    setup_logging(paths)

    cfg_dict = read_config_yaml(paths)
    retort = get_base_retort()
    mq_config = load_config(cfg_dict, paths, retort)

    rabbit_broker = RabbitBroker(url=mq_config.mq.uri)
    mq_app = FastStream(rabbit_broker)

    di_container = make_async_container(
        *get_common_providers(),
        FastStreamProvider(),
        context={MQAppConfig: mq_config}
    )
    setup_dishka_faststream(di_container, mq_app)

    tasks.setup(rabbit_broker)

    return mq_app


async def run():
    mq_app = main()
    await mq_app.run()


if __name__ == '__main__':
    asyncio.run(run())
