from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy.orm import Session

from goToVladi.core.data.db import models as db


def setup(app: Flask):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    @inject
    def load_user(user_id, session: FromDishka[Session]):
        return session.query(db.User).get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("admin.login_view"))
