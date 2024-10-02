from flask_admin.model import InlineFormAdmin

from goToVladi.flaskadmin.views.mixins.media import MediaMixin

from flask_admin.contrib.sqla.form import get_form
class MediaInline(MediaMixin, InlineFormAdmin):
    pass
