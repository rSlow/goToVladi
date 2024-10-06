from flask_admin import BaseView, expose, Admin
from sqlalchemy.orm import Session, scoped_session

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


class MailingView(BaseView):
    def __init__(
            self, session: scoped_session[Session], config: FlaskAppConfig,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.session = session
        self.config = config

    @expose('/')
    def index(self):
        return self.render("custom_admin/base.html")

    @expose("/send", methods=["GET", "POST"])
    def send_mailing(self):
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
