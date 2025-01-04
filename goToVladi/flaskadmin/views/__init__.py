__all__ = [
    "mount_admin_views",
    "mount_views"
]

from flask import Flask, Blueprint
from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session, configure_mappers

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.views import media, errors
from .hotels import mount_hotel_views
from .mailing import mount_mailing_view
from .massages import mount_massages_views
from .regions import mount_region_views
from .restaurants import mount_restaurant_views
from .trips import mount_trips_views
from .users import mount_users_views


def mount_admin_views(admin_app: Admin, session: scoped_session[Session]):
    configure_mappers()

    mount_region_views(admin_app, session)
    mount_restaurant_views(admin_app, session)
    mount_hotel_views(admin_app, session)
    mount_trips_views(admin_app, session)
    mount_massages_views(admin_app, session)
    mount_users_views(admin_app, session)

    mount_mailing_view(admin_app)


def mount_views(app: Flask, config: FlaskAppConfig):
    root_router = Blueprint(
        'root', __name__,
        url_prefix=config.flask.get_real_root_path(config.web.root_path)
    )

    errors.setup(app)

    # mount blueprints to the root router
    if config.flask.debug:
        root_router.register_blueprint(media.setup(config))

    app.register_blueprint(root_router)
