from dataclasses import dataclass

from goToVladi.core.config import BaseConfig


@dataclass
class MQAppConfig(BaseConfig):
    @classmethod
    def from_base(cls, base: BaseConfig):
        return MQAppConfig(
            app=base.app, paths=base.paths, db=base.db, redis=base.redis,
            web=base.web, static=base.static, mq=base.mq, auth=base.auth
        )
