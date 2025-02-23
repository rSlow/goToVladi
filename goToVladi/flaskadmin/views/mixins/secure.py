from flask import url_for, redirect
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class SecureViewMixin:
    def is_accessible(self):
        return current_user.is_authenticated \
            and current_user.is_superuser \
            and current_user.is_active

    def _handle_view(self, *_, **__):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view'))


