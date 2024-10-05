from flask import Flask, Blueprint
from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session, configure_mappers

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.views import media
from goToVladi.flaskadmin.views.hotels import mount_hotel_views
from goToVladi.flaskadmin.views.regions import mount_region_views
from goToVladi.flaskadmin.views.restaurants import mount_restaurant_views
from goToVladi.flaskadmin.views.trips import mount_trips_views


def mount_admin_views(admin_app: Admin, session: scoped_session[Session]):
    configure_mappers()

    mount_region_views(admin_app, session)
    mount_restaurant_views(admin_app, session)
    mount_hotel_views(admin_app, session)
    mount_trips_views(admin_app, session)


def mount_views(app: Flask, cfg: FlaskAppConfig):
    root_router = Blueprint('root', __name__, url_prefix=cfg.flask.root_path)

    # mount views to the root router
    root_router.add_url_rule(
        cfg.admin.media_url + '/<storage>/<file_id>',
        None,
        media.serve_media, methods=["GET"]
    )

    app.register_blueprint(root_router)
