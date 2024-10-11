from dishka import make_container
from dishka.integrations.flask import setup_dishka as setup_dishka_flask
from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import scoped_session

from goToVladi.core.config import setup_logging, BaseConfig
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.data.db.utils.file_field import configure_storages
from goToVladi.core.di import get_common_sync_providers
from goToVladi.core.factory import db
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.config.parser.main import load_config
from goToVladi.flaskadmin.di import get_flask_providers
from goToVladi.flaskadmin.utils import i18n, scss, auth
from goToVladi.flaskadmin.views import mount_admin_views, mount_views
from goToVladi.flaskadmin.views.index import AdminIndexView


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    flask_config = load_config(paths, retort)

    flask_app = Flask(
        flask_config.app.name,
        template_folder=flask_config.paths.admin_path / "templates",
        static_folder=flask_config.paths.admin_path / "static",
        static_url_path=(
                flask_config.flask.root_path + flask_config.admin.static_path
        )
    )
    flask_app.config["SECRET_KEY"] = flask_config.flask.secret_key

    di_container = make_container(
        *get_common_sync_providers(),
        *get_flask_providers(),
        context={
            BaseConfig: flask_config.as_base(),
            FlaskAppConfig: flask_config
        }
    )
    setup_dishka_flask(di_container, flask_app)

    sqlalchemy_session = scoped_session(db.sync.create_pool(flask_config.db))

    admin = Admin(
        flask_app,
        url=flask_config.flask.root_path,
        name=flask_config.app.name,
        index_view=AdminIndexView(
            name="Главная страница",
            url=flask_config.flask.root_path,
            template="self_admin/index.html",

        ),
        base_template="self_admin/base.html",
        template_mode=flask_config.admin.template_mode,
        static_url_path=flask_config.admin.static_path + "-admin"
        # "-admin" prefix for not matching as base static, cause in admin
        # templates is used `admin_static.url()` marco
    )

    mount_admin_views(admin, sqlalchemy_session)
    mount_views(flask_app, flask_config)

    configure_storages(
        upload_path=paths.upload_file_path,
        storages=flask_config.db.file_storages
    )
    auth.setup(flask_app)
    i18n.setup(flask_app)
    scss.setup(flask_app, flask_config)

    return flask_app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=8000)
