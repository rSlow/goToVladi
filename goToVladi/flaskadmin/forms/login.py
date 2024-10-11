from wtforms import form as forms, fields, validators


class LoginForm(forms.Form):
    username = fields.StringField(
        label="Логин",
        validators=[validators.InputRequired()],
        render_kw={"placeholder": "Введите логин"}
    )
    password = fields.PasswordField(
        label="Пароль",
        validators=[validators.InputRequired()],
        render_kw={"placeholder": "Введите пароль"}
    )
