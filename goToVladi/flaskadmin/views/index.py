import flask_login
from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import redirect, url_for, request, flash, get_flashed_messages
from flask_admin import AdminIndexView as BaseAdminIndexView, expose, helpers
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from goToVladi.core.utils.auth.hash import check_tg_auth
from goToVladi.core.utils.auth.models import UserTgAuth
from goToVladi.flaskadmin import crud
from goToVladi.flaskadmin.config.models import FlaskAppConfig
from goToVladi.flaskadmin.forms.login import LoginForm
from goToVladi.flaskadmin.utils import exceptions as exc
from goToVladi.flaskadmin.utils.auth import AuthService


class AdminIndexView(BaseAdminIndexView):
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

            except exc.FormError as ex:
                form.form_errors.append(ex.message)

        form_errors = get_flashed_messages(with_categories=True, category_filter=["form-error"])
        form.form_errors.extend([error for _, error in form_errors])

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
    def tg_auth_data(self, session: FromDishka[Session], config: FromDishka[FlaskAppConfig]):
        if user_data := dict(request.args):
            try:
                tg_user = UserTgAuth.model_validate(user_data)
                check_tg_auth(tg_user, config.auth.tg_bot_token)
                user = crud.user.get_by_tg_id(tg_user.id, session)
                if not user.is_superuser:
                    raise exc.AccessDeniedError
                flask_login.login_user(user)
                return redirect(url_for(".index"))
            except NoResultFound:
                flash(exc.AccessDeniedError.message, category="form-error")
            except exc.FormError as ex:
                flash(ex.message, category="form-error")

        return redirect(url_for(".login_view"))
