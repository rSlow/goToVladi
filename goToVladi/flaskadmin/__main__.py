from dishka import make_container
from dishka.integrations.flask import setup_dishka as setup_dishka_flask
from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import scoped_session

from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.config.parser.retort import get_base_retort
from goToVladi.core.data.db.utils.file_field import configure_storage
from goToVladi.core.factory import db
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.config.parser.main import load_config
from goToVladi.flaskadmin.di.config import ConfigProvider
from goToVladi.flaskadmin.di.context import FlaskInjectContext
from goToVladi.flaskadmin.di.db import SyncDbProvider
from goToVladi.flaskadmin.utils.logging import setup_logging
from goToVladi.flaskadmin.utils.login import init_flask_login
from goToVladi.flaskadmin.views import mount_admin_views, mount_views
from goToVladi.flaskadmin.views.admin import AdminIndexView


def main():
    setup_logging()

    paths = get_paths()
    config = read_config_yaml(paths)
    retort = get_base_retort()
    flask_config = load_config(config, paths, retort)

    flask_app = Flask(
        import_name=flask_config.app.name,
        template_folder=flask_config.paths.admin_path / "templates",
        static_folder=flask_config.paths.admin_path / "static",
    )
    flask_app.secret_key = flask_config.flask.secret_key

    di_container = make_container(
        ConfigProvider(),
        SyncDbProvider(),
        context={FlaskAppConfig: flask_config}
    )
    FlaskInjectContext.container = di_container  # for use in admin
    setup_dishka_flask(di_container, flask_app)

    sqlalchemy_session = scoped_session(db.sync.create_pool(flask_config.db))

    admin = Admin(
        flask_app,
        url=flask_config.flask.root_path,
        name=flask_config.app.name,
        index_view=AdminIndexView(url=flask_config.flask.root_path),
        template_mode=flask_config.admin.template_mode,
    )
    mount_admin_views(admin, sqlalchemy_session)
    mount_views(flask_app, flask_config)

    configure_storage(paths.upload_file_path)
    init_flask_login(flask_app)

    return flask_app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
