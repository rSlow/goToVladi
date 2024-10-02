from flask_admin.model import InlineFormAdmin

from goToVladi.flaskadmin.views.mixins.media import MediaMixin


class MediaInline(MediaMixin, InlineFormAdmin):
    pass
