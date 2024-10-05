import flask_login
from dishka import FromDishka
from flask import redirect, url_for, request, render_template, flash
from flask_admin import AdminIndexView as BaseAdminIndexView, expose, helpers
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session
from wtforms import form as forms, fields, validators

from goToVladi.core.data.db import models as db
from goToVladi.flaskadmin.di.context import FlaskInjectContext


class LoginForm(forms.Form):
    username = fields.StringField(
        label="Логин",
        validators=[validators.InputRequired()]
    )
    password = fields.PasswordField(
        label="Пароль",
        validators=[validators.InputRequired()]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @FlaskInjectContext.sync_inject
    def get_user(self, session: FromDishka[Session]):
        username = self.username.data
        password = self.password.data
        result = session.scalars(
            select(db.User)
            .where(db.User.username == username)
        )
        try:
            user = result.one()
        except (MultipleResultsFound, NoResultFound):
            return

        if user.is_superuser and user.id is not None \
                and self.pwd_context.verify(password, user.hashed_password):
            return user


class AdminIndexView(BaseAdminIndexView):

    @expose("/")
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super().index()

    @expose("/login/", methods=["GET", "POST"])
    def login_view(self):
        form = LoginForm(request.form)
        self._template_args['form'] = form

        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user:
                flask_login.login_user(user)
            else:
                flash("Invalid credentials", category="error")
        if flask_login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        return render_template("auth/login.html", form=form)

    @expose("/logout/")
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for(".index"))
