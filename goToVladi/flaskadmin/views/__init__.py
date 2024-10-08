__all__ = [
    "mount_admin_views",
    "mount_views"
]

from flask import Flask, Blueprint
from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session, configure_mappers

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.views import media
from goToVladi.flaskadmin.views.hotels import mount_hotel_views
from goToVladi.flaskadmin.views.mailing import mount_mailing_view
from goToVladi.flaskadmin.views.regions import mount_region_views
from goToVladi.flaskadmin.views.restaurants import mount_restaurant_views
from goToVladi.flaskadmin.views.trips import mount_trips_views
from goToVladi.flaskadmin.views.users import mount_users_views


def mount_admin_views(
        admin_app: Admin, session: scoped_session[Session],
        config: FlaskAppConfig,
):
    configure_mappers()

    mount_region_views(admin_app, session)
    mount_restaurant_views(admin_app, session)
    mount_hotel_views(admin_app, session)
    mount_trips_views(admin_app, session)
    mount_users_views(admin_app, session)

    mount_mailing_view(admin_app, session, config)


def mount_views(app: Flask, config: FlaskAppConfig):
    root_router = Blueprint('root', __name__, url_prefix=config.flask.root_path)

    # mount blueprints to the root router
    root_router.register_blueprint(media.setup(config))

    app.register_blueprint(root_router)
