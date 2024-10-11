from dataclasses import dataclass

from goToVladi.core.config import BaseConfig
from goToVladi.flaskadmin.config.models.admin import FlaskAdminConfig
from goToVladi.flaskadmin.config.models.flask import FlaskConfig
from goToVladi.flaskadmin.config.models.static import FlaskStaticConfig


@dataclass
class FlaskAppConfig(BaseConfig):
    flask: FlaskConfig
    admin: FlaskAdminConfig
    static: FlaskStaticConfig

    @classmethod
    def from_base(
            cls, base: BaseConfig, flask: FlaskConfig, admin: FlaskAdminConfig,
            static: FlaskStaticConfig
    ):
        return FlaskAppConfig(
            app=base.app, paths=base.paths, db=base.db, redis=base.redis,
            web=base.web, media=base.media, mq=base.mq, auth=base.auth,
            flask=flask, admin=admin, static=static
        )
