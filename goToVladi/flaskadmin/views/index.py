import flask_login
from adaptix import Retort
from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import redirect, url_for, request
from flask_admin import AdminIndexView as BaseAdminIndexView, expose, helpers
from flask_login import login_required, current_user
from sqlalchemy.orm import Session

from goToVladi.core.utils.auth.models import UserTgAuth
from goToVladi.core.utils.exceptions.auth import AuthError
from goToVladi.flaskadmin import crud
from goToVladi.flaskadmin.config.models import FlaskAppConfig
from goToVladi.flaskadmin.forms.login import LoginForm
from goToVladi.flaskadmin.utils.auth import AuthService


class AdminIndexView(BaseAdminIndexView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retort = Retort()

    @expose("/")
    def index(self):
        if not current_user.is_authenticated or not current_user.is_superuser:
            return redirect(url_for(".login_view"))
        return super().index()

    @expose("/login/", methods=["GET", "POST"])
    @inject
    def login_view(
            self, auth_service: FromDishka[AuthService],
            session: FromDishka[Session], config: FromDishka[FlaskAppConfig]
    ):
        form = LoginForm(request.form)
        self._template_args['form'] = form

        if helpers.validate_form_on_submit(form):
            try:
                user = auth_service.authenticate_user(
                    username=form.username.data,
                    password=form.password.data,
                    session=session
                )
                if user:
                    flask_login.login_user(user)
            except AuthError as ex:
                form.form_errors.append(ex.args[0])

        if current_user.is_authenticated and current_user.is_superuser:
            return redirect(url_for(".index"))

        return self.render(
            "auth/login.html", form=form,
            tg_auth_config={
                "bot_username": config.auth.tg_bot_username,
                "auth_url": config.web.base_url + url_for(".tg_auth_data"),
            }
        )

    @expose("/logout/")
    @login_required
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for(".index"))

    @expose("/tg-auth/data/", methods=["GET", "POST"])
    @inject
    def tg_auth_data(self, session: FromDishka[Session]):
        user_data = request.args
        user = UserTgAuth(
            id=user_data.get("id"),
            first_name=user_data.get("first_name"),
            auth_date=user_data.get("auth_date"),
            hash=user_data.get("hash"),
            photo_url=user_data.get("photo_url"),
            username=user_data.get("username"),
            last_name=user_data.get("last_name"),
        ).to_dto()
        saved_user = crud.upsert_user(user, session)
        if saved_user.is_superuser:
            flask_login.login_user(saved_user)
        return redirect(url_for(".index"))
