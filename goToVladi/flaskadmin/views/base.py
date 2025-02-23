from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView

from goToVladi.flaskadmin.views.mixins.column_label import ColumnLabelMixin
from goToVladi.flaskadmin.views.mixins.columns import ColumnListEqualFiltersMixin
from goToVladi.flaskadmin.views.mixins.secure import SecureViewMixin


class SecureView(BaseView, SecureViewMixin):
    pass


class AppModelView(ModelView,
                   SecureViewMixin,
                   ColumnLabelMixin,
                   ColumnListEqualFiltersMixin):
    page_size = 10
