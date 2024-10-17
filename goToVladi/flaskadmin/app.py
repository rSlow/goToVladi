from dishka import make_container
from dishka.integrations.flask import setup_dishka as setup_dishka_flask
from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import scoped_session

from goToVladi.core.config import setup_logging, BaseConfig
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.data.db.utils.storage import configure_storages
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
    config = load_config(paths, retort)

    flask_app = Flask(
        config.app.name,
        template_folder=config.paths.admin_path / "templates",
        static_folder=config.paths.admin_path / "static",
        static_url_path=(
                config.flask.get_real_root_path(config.web.root_path)
                + config.static.base_url
        )
    )
    flask_app.config.update({
        "SECRET_KEY": config.flask.secret_key,
        "DEBUG": config.flask.debug,
        "FLASK_ADMIN_FLUID_LAYOUT": config.admin.fluid
    })

    di_container = make_container(
        *get_common_sync_providers(),
        *get_flask_providers(),
        context={
            BaseConfig: config.as_base(),
            FlaskAppConfig: config
        }
    )
    setup_dishka_flask(di_container, flask_app)

    sqlalchemy_session = scoped_session(db.sync.create_pool(config.db))

    root_path = config.flask.get_real_root_path(config.web.root_path)
    admin = Admin(
        flask_app,
        url=root_path,
        name=config.app.name,
        index_view=AdminIndexView(
            name="Главная страница",
            url=root_path,
            template="self_admin/index.html",
        ),
        base_template="self_admin/base.html",
        template_mode=config.admin.template_mode,
        static_url_path=config.static.base_url + "-admin"
        # "-admin" prefix for not matching as base static, cause in admin
        # templates is used {{ admin_static.url() }} marco
    )

    mount_admin_views(admin, sqlalchemy_session)
    mount_views(flask_app, config)

    configure_storages(
        upload_path=paths.media_path,
        storages=config.db.file_storages
    )
    auth.setup(flask_app)
    i18n.setup(flask_app)

    if config.flask.debug:
        scss.setup(flask_app, config)
    else:
        scss.compile_files(config)

    return flask_app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
