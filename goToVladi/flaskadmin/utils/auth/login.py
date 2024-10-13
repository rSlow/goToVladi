from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy.orm import Session

from goToVladi.core.data.db import dto
from goToVladi.flaskadmin import crud


def setup(app: Flask):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    @inject
    def load_user(user_id, session: FromDishka[Session]) -> dto.User:
        return crud.user.get(user_id, session)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("admin.login_view"))
