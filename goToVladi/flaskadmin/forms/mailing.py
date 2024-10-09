from wtforms import fields, validators
from wtforms.form import Form


class MailingForm(Form):
    message = fields.TextAreaField(
        label="Сообщение",
        validators=[validators.DataRequired()]
    )
