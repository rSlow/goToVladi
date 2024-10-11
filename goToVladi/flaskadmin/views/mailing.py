from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import url_for, request, flash, redirect
from flask_admin import expose, Admin
from flask_admin.helpers import validate_form_on_submit
from pika.adapters.blocking_connection import BlockingChannel

from goToVladi.flaskadmin.forms.mailing import MailingForm
from goToVladi.flaskadmin.utils.secure_view import SecureView


class MailingView(SecureView):

    @expose('/', methods=["GET", "POST"])
    @inject
    def index(self, mq: FromDishka[BlockingChannel]):
        if request.method == "POST":
            form = MailingForm(request.form)
        else:
            form = MailingForm()

        if validate_form_on_submit(form):
            mail_data = form.message.data
            mq.basic_publish("mail", "all", mail_data)
            flash("Сообщение успешно отправлено!", "success")
            return redirect(url_for("admin.index"))

        return self.render(
            "mailing/index.html",
            form=form, return_url=url_for("admin.index"),
        )

    @expose("/pre-send", methods=["GET", "POST"])
    def pre_send_mailing(self):
        ...


def mount_mailing_view(admin_app: Admin):
    admin_app.add_view(
        MailingView(name="Рассылка", endpoint="mailing")
    )
