from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import scoped_session, Session, configure_mappers

from goToVladi.flaskadmin.views import static
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


def mount_views(app: Flask):
    app.add_url_rule(
        '/static/<storage>/<file_id>', None,
        static.serve_files, methods=["GET"]
    )
