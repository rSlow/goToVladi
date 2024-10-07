from flask_admin.model import InlineFormAdmin

from goToVladi.flaskadmin.fields.file import SQLAlchemyInlineAttachmentField


class MediaInline(InlineFormAdmin):
    form_overrides = {
        "content": SQLAlchemyInlineAttachmentField
    }
    column_labels = {
        "content": ""
    }
