from flask_admin.form import FileUploadField

from goToVladi.core.config import Paths


def file_upload_field(_paths: Paths):
    def wrapper(*args, **kwargs):
        return FileUploadField(
            *args, **kwargs,
            base_path=_paths.upload_file_path,
        )

    return wrapper
