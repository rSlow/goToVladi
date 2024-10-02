from goToVladi.flaskadmin.fields.file import SQLAlchemyFileUploadField


class MediaMixin:
    form_overrides = {
        "content": SQLAlchemyFileUploadField
    }
