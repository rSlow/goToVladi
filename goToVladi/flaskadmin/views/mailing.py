from flask import url_for, request, flash, redirect
from flask_admin import expose, Admin
from flask_admin.helpers import validate_form_on_submit
from sqlalchemy.orm import Session, scoped_session

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.forms.mailing import MailingForm
from goToVladi.flaskadmin.utils.secure_view import SecureView


class MailingView(SecureView):
    def __init__(
            self, session: scoped_session[Session], config: FlaskAppConfig,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.session = session
        self.config = config

    @expose('/', methods=["GET", "POST"])
    def index(self):
        if request.method == "POST":
            form = MailingForm(request.form)
        else:
            form = MailingForm()

        if validate_form_on_submit(form):
            mail_data = form.message.data
            ...
            flash("Сообщение успешно отправлено!", "success")
            return redirect(url_for("admin.index"))

        return self.render(
            "mailing/index.html",
            form=form, return_url=url_for("admin.index"),
        )

    @expose("/pre-send", methods=["GET", "POST"])
    def pre_send_mailing(self):
        ...


def mount_mailing_view(
        admin_app: Admin, session: scoped_session[Session],
        config: FlaskAppConfig
):
    admin_app.add_view(
        MailingView(
            session=session, config=config,
            name="Рассылка",
            # category="Рассылка",
            endpoint="mailing",
        )
    )
