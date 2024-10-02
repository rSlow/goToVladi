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
from goToVladi.flaskadmin.config.parser.main import load_config
from goToVladi.flaskadmin.views import mount_admin_views, mount_views


def main():
    paths = get_paths()
    config = read_config_yaml(paths)
    retort = get_base_retort()
    flask_config = load_config(config, paths, retort)

    flask_app = Flask(flask_config.app.name)
    flask_app.secret_key = flask_config.flask.secret_key

    di_container = make_container(
        # TODO pass providers
        context={"flask_config": flask_config}
    )
    setup_dishka_flask(di_container, flask_app)

    sqlalchemy_session = scoped_session(db.sync.create_pool(flask_config.db))

    admin = Admin(
        flask_app,
        name=flask_config.app.name,
        template_mode=flask_config.admin.template_mode,
    )
    mount_admin_views(admin, sqlalchemy_session)
    mount_views(flask_app)

    configure_storage(paths.upload_file_path)

    return flask_app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
