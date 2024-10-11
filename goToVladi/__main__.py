import logging
from functools import partial

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from goToVladi.api import create_app as create_api_app, ApiAppConfig
from goToVladi.api.config.models.api import ApiConfig
from goToVladi.api.config.parser.main import load_config as load_api_config
from goToVladi.api.di import get_api_providers
from goToVladi.api.utils.webhook.handler import SimpleRequestHandler
from goToVladi.api.utils.webhook.setup import setup_lifespan
from goToVladi.bot.config.models import BotAppConfig
from goToVladi.bot.config.models.webhook import WebhookConfig
from goToVladi.bot.config.parser.main import load_config as load_bot_config
from goToVladi.bot.di import get_bot_providers
from goToVladi.bot.utils import ui
from goToVladi.core.config import BaseConfig
from goToVladi.core.config.models.web import WebConfig
from goToVladi.core.config.parser.config_logging import setup_logging
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.data.db.utils.file_field import configure_storages
from goToVladi.core.di import get_common_providers
from goToVladi.core.utils import di_visual

logger = logging.getLogger("goToVladi")


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()

    api_config = load_api_config(paths, retort)
    bot_config = load_bot_config(paths, retort)
    webhook_config = bot_config.bot.webhook

    di_container = make_async_container(
        *get_common_providers(),
        *get_bot_providers(),
        *get_api_providers(),
        context={
            BaseConfig: api_config.as_base(),
            ApiAppConfig: api_config,
            BotAppConfig: bot_config,
        }
    )
    api_app = create_api_app(api_config)
    setup_lifespan(api_app, di_container)

    webhook_handler = SimpleRequestHandler(secret_token=webhook_config.secret)
    webhook_handler.register(api_app, webhook_config.path)

    setup_fastapi_dishka(di_container, api_app)

    startup_callback = partial(
        on_startup,
        di_container, api_config.web, api_config.api, webhook_config
    )
    shutdown_callback = partial(on_shutdown, di_container)
    api_app.add_event_handler("startup", startup_callback)
    api_app.add_event_handler("shutdown", shutdown_callback)

    configure_storages(
        upload_path=paths.upload_file_path,
        storages=bot_config.db.file_storages
    )

    logger.info(
        "app prepared with dishka:\n%s",
        di_visual.render(
            [di_container.registry, *di_container.child_registries]
        ),
    )
    return api_app


async def on_startup(
        dishka: AsyncContainer,
        web_config: WebConfig, api_config: ApiConfig,
        webhook_config: WebhookConfig
):
    webhook_url = web_config.get_real_base_url(
        api_config.root_path
    ) + webhook_config.path

    bot = await dishka.get(Bot)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_config.secret,
    )
    logger.info("as webhook url used %s", webhook_url)

    await ui.setup(bot)
    await dishka.get(Dispatcher)  # initialize dispatcher


async def on_shutdown(dishka: AsyncContainer):
    bot: Bot = await dishka.get(Bot)
    await bot.delete_webhook()
    logger.info("webhook deleted")

    await dishka.close()


def run():
    uvicorn.run(
        app="goToVladi.__main__:main",
        host="0.0.0.0",
        port=8000,
        factory=True
    )


if __name__ == '__main__':
    run()
