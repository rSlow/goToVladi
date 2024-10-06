from flask import Flask

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.utils.sass.builder import Manifest
from goToVladi.flaskadmin.utils.sass.wsgi import SassMiddleware


def setup(app: Flask, config: FlaskAppConfig):
    static_path = config.paths.admin_path / "static"
    app.wsgi_app = SassMiddleware(
        app=app.wsgi_app,
        manifests={
            "app": Manifest(
                sass_path=(static_path / "sass").as_posix(),
                css_path=(static_path / "css" / "c").as_posix(),
                wsgi_path='/static/css/c',
                strip_extension=False
            ),
        },
        source_map=False,
        output_style="compressed",
    )
