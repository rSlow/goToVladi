from dataclasses import dataclass

from goToVladi.core.config import BaseConfig
from goToVladi.flaskadmin.config.models.admin import FlaskAdminConfig
from goToVladi.flaskadmin.config.models.flask import FlaskConfig


@dataclass
class FlaskAppConfig(BaseConfig):
    flask: FlaskConfig
    admin: FlaskAdminConfig

    @classmethod
    def from_base(
            cls, base: BaseConfig, flask: FlaskConfig, admin: FlaskAdminConfig
    ):
        return FlaskAppConfig(
            app=base.app, paths=base.paths, db=base.db, redis=base.redis,
            web=base.web, static=base.static, mq=base.mq, auth=base.auth,
            flask=flask, admin=admin
        )
