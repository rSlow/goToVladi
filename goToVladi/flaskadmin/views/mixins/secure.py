from flask import url_for, redirect
from flask_login import current_user

from goToVladi.flaskadmin.utils.auth.rights import has_admin_panel_rights


class SecureViewMixin:
    def is_accessible(self):
        return current_user.is_authenticated and has_admin_panel_rights(current_user)

    is_visible = is_accessible

    def _handle_view(self, *_, **__):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view'))
