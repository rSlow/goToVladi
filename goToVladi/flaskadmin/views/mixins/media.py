from goToVladi.core.config.parser.paths import get_paths
from goToVladi.flaskadmin.fields.file import file_upload_field

paths = get_paths()


class MediaMixin:
    form_overrides = {
        "content": file_upload_field(paths)
    }
