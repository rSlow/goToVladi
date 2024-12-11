import os.path as op
import typing
from pathlib import Path

from dishka import FromDishka
from dishka.integrations.flask import inject
from flask_admin.babel import gettext
from flask_admin.form import FileUploadField, BaseForm
from markupsafe import Markup
from multidict import MultiDict
from sqlalchemy_file import File
from werkzeug.datastructures import FileStorage
from wtforms import ValidationError
from wtforms.utils import unset_value
from wtforms.widgets import html_params

from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.data.db.models.mixins import AttachmentProtocol
from goToVladi.core.data.db.utils import file_field
from goToVladi.flaskadmin.config.models import FlaskAppConfig
from .main import SQLAlchemyFileUploadInput


class SQLAlchemyInlineAttachmentUploadInput(SQLAlchemyFileUploadInput):
    file_template = (
            "<div class='file-widget'> "
            "  <a %(a)s class='file-link'>%(filename)s</a>"
            "  <a %(a)s download>Скачать</a>"
            "</div>" + SQLAlchemyFileUploadInput.empty_template
    )
    image_template = (
            "<div class='file-widget'>"
            "  <a %(a)s class='image-container'>"
            "    <img %(img)s>"
            "  </a>"
            "  <a %(a)s download>Скачать</a>"
            "</div>" + SQLAlchemyFileUploadInput.empty_template
    )
    image_extensions = ('gif', 'jpg', 'jpeg', 'png', 'tiff')

    def __call__(self, field: FileUploadField, **kwargs):
        data = field.data
        if data and isinstance(data, File):
            if self._is_file_image(data.file.filename):
                return self._render_image(field, **kwargs)
            return self._render_file(field, **kwargs)
        return self.empty_template

    def _render_file(self, field: FileUploadField, **kwargs):
        template = self.verify_template(field, self.file_template)
        file = typing.cast(File, field.data)
        filename = file.file.filename
        media_url = self.get_media_url(
            file=file, media_path=field.base_path  # type:ignore
        )  # type:ignore

        args = self._get_base_args(field, **kwargs)
        args["a"] = html_params(href=media_url, target="_blank")
        args["filename"] = filename

        return Markup(template % args)

    def _render_image(self, field: FileUploadField, **kwargs):
        template = self.verify_template(field, self.image_template)
        media_url = self.get_media_url(
            file=field.data, media_path=field.base_path  # type:ignore
        )  # type:ignore

        args = self._get_base_args(field, **kwargs)
        args["a"] = html_params(href=media_url, target="_blank")
        args["img"] = html_params(src=media_url)

        return Markup(template % args)

    @staticmethod
    @inject
    def get_media_url(
            file: File, media_path: Path, config: FromDishka[FlaskAppConfig]
    ):
        if config.flask.debug:
            root_path = config.flask.get_real_root_path(config.web.root_path)
            media_prefix = root_path + config.admin.media_url + "/"
            return media_prefix + file["path"]

        root_path = config.web.root_path or ""
        relative_url = file_field.get_relative_path(file["url"], media_path)
        return root_path + config.media.base_url + "/" + relative_url.as_posix()

    @staticmethod
    def _get_file_extension(filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()

    def _is_file_image(self, filename: str):
        return self._get_file_extension(filename) in self.image_extensions


class SQLAlchemyInlineAttachmentField(FileUploadField):
    widget = SQLAlchemyInlineAttachmentUploadInput()
    data: FileStorage | None

    def __init__(
            self, label=None, validators=None, base_path=None,
            relative_path=None, namegen=None, allowed_extensions=None,
            permission=0o666, allow_overwrite=True,
            render_image: bool = True, max_size: int = 200,
            **kwargs
    ):
        """
            The field form to use in conjunction with sqlalchemy_file.
            Use in form_overrides attribute of ModevView class.
            params copied from parent class.
        """
        super().__init__(
            label=label, validators=validators, relative_path=relative_path,
            namegen=namegen, allowed_extensions=allowed_extensions,
            permission=permission, allow_overwrite=allow_overwrite,
            **kwargs
        )
        self.base_path = base_path or get_paths().media_path
        self.render_image = render_image
        self.max_size = max_size

    @staticmethod
    def _is_file_valid_to_save(data: FileStorage):
        if data:
            return any((
                isinstance(data, FileStorage) and data.filename,
                isinstance(data, File) and not data["saved"]
            ))
        return False

    def pre_validate(self, form: BaseForm):
        if not self.is_file_allowed(self.data.filename):
            raise ValidationError(gettext("Invalid file extension"))

        # Handle overwriting existing content
        if not self._is_file_valid_to_save(self.data):
            return

        if not self._allow_overwrite and self._check_exists(self.data.url):
            raise ValidationError(
                gettext(f"File {self.data.filename} already exists.")
            )

    def process(
            self, formdata: MultiDict, data=unset_value,
            extra_filters: list | None = None
    ):
        if formdata:
            marker = '_%s-delete' % self.name
            if marker in formdata:
                self._should_delete = True

        super().process(formdata, data, extra_filters)

    def process_formdata(self, valuelist: list[FileStorage]):
        if self._should_delete:
            self.data = None
        elif valuelist:
            for data in valuelist:
                if self._is_file_valid_to_save(data):
                    self.data = data
                    break

    def populate_obj(self, obj: AttachmentProtocol, name: str):
        field = getattr(obj, name, None)
        if field:
            # If field should be deleted, clean it up
            if self._should_delete:
                setattr(obj, name, None)
                return

        if self._is_file_valid_to_save(self.data):
            setattr(
                obj, name,
                obj.__upload_type__(
                    content_type=self.data.content_type,
                    filename=self.data.filename,
                    content=self.data.stream
                )
            )

    @staticmethod
    def _check_exists(path: str):
        return op.exists(path) and op.isfile(path)
