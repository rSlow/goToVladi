# Initialize flask-login
import flask_login
from dishka import FromDishka
from flask import Flask
from sqlalchemy.orm import Session

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.di.context import FlaskInjectContext


def init_flask_login(app: Flask):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    @FlaskInjectContext.sync_inject
    def load_user(user_id, session: FromDishka[Session]):
        return session.query(db.User).get(user_id)
