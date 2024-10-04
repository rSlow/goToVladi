from flask_admin.model import InlineFormAdmin

from goToVladi.flaskadmin.fields.file import SQLAlchemyFileUploadField


class MediaInline(InlineFormAdmin):
    form_overrides = {
        "content": SQLAlchemyFileUploadField
    }
    column_labels = {
        "content": ""
    }
