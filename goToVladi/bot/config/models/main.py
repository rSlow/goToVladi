from dataclasses import dataclass

from goToVladi.bot.config.models.bot import BotConfig
from goToVladi.bot.config.models.storage import StorageConfig
from goToVladi.core.config import BaseConfig


@dataclass
class BotAppConfig(BaseConfig):
    bot: BotConfig
    storage: StorageConfig

    @classmethod
    def from_base(
            cls, base: BaseConfig, bot: BotConfig, storage: StorageConfig
    ):
        return cls(
            paths=base.paths, db=base.db, redis=base.redis, app=base.app,
            web=base.web, media=base.media, mq=base.mq, auth=base.auth,
            bot=bot, storage=storage
        )
