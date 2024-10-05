import os.path as op
import typing

from dishka import FromDishka
from flask_admin.babel import gettext
from flask_admin.form import FileUploadField, BaseForm
from markupsafe import Markup
from sqlalchemy_file import File
from werkzeug.datastructures import FileStorage
from wtforms import ValidationError
from wtforms.utils import unset_value
from wtforms.widgets import html_params

from goToVladi.core.config.parser.paths import get_paths
from goToVladi.core.data.db.models.base_attachment import BaseAttachment
from goToVladi.flaskadmin.config.models.main import FlaskAppConfig
from goToVladi.flaskadmin.di.context import FlaskInjectContext


class SQLAlchemyUploadInput:
    empty_template = '<input %(file)s>'
    input_type = 'file'
    file_template = (
        "<div> "
        "  <a %(a)s>%(url)s</a> | "
        "  <a %(a)s download>Скачать</a>"
        "</div>"
        "<input %(file)s>"
    )
    image_template = (
        "<div>"
        "  <a %(a)s>"
        "    <img %(img)s>"
        "  </a>"
        "  <a %(a)s download>Скачать</a>"
        "</div>"
        "<input %(file)s>"
    )
    image_extensions = ('gif', 'jpg', 'jpeg', 'png', 'tiff')

    @staticmethod
    def _get_base_args(field: FileUploadField, **kwargs) -> dict:
        value = field.data or ""
        return {
            "text": html_params(
                type="text", readonly="readonly", value=value,
                name=field.name
            ),
            "file": html_params(
                type="file", value=value,
                style="padding: 10px 0 0",
                **kwargs
            ),
            "marker": '_%s-delete' % field.name,
        }

    def __call__(self, field: FileUploadField, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        data = field.data
        if data and isinstance(data, File):
            if self._is_file_image(data.file.filename):
                return self._render_image(field, **kwargs)
        return self._render_file(field, **kwargs)

    def _render_file(self, field: FileUploadField, **kwargs):
        template = self.file_template if field.data else self.empty_template
        if field.errors:
            template = self.empty_template

        args = self._get_base_args(field, **kwargs)
        if isinstance(field.data, File):
            url = field.data.path
            media_url = self._get_media_prefix() + url

            args["a"] = html_params(href=media_url, target="_blank")
            args["url"] = url

        return Markup(template % args)

    def _render_image(self, field: FileUploadField, **kwargs):
        template = self.image_template if field.data else self.empty_template
        if field.errors:
            template = self.empty_template

        value = typing.cast(File, field.data)
        url = value.path
        media_url = self._get_media_prefix() + url

        args = self._get_base_args(field, **kwargs)
        args["a"] = html_params(href=media_url, target="_blank")
        args["url"] = url
        args["img"] = html_params(
            src=media_url, style="width:200px; height: auto"
        )

        return Markup(template % args)

    @staticmethod
    @FlaskInjectContext.sync_inject
    def _get_media_prefix(config: FromDishka[FlaskAppConfig]):
        return config.flask.root_path + config.admin.media_url + "/"

    @staticmethod
    def _get_file_extension(filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()

    def _is_file_image(self, filename: str):
        return self._get_file_extension(filename) in self.image_extensions


class SQLAlchemyFileUploadField(FileUploadField):
    widget = SQLAlchemyUploadInput()
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
        self.base_path = base_path or get_paths().upload_file_path
        self.render_image = render_image
        self.max_size = max_size

    @staticmethod
    def _is_file_uploaded(data: FileStorage):
        if data:
            return any((
                isinstance(data, FileStorage) and data.filename,
                isinstance(data, File) and not data["saved"]
            ))
        return False

    def pre_validate(self, form: BaseForm):
        if all((
                self._is_file_uploaded(self.data),
                not self.is_file_allowed(self.data.filename)
        )):
            raise ValidationError(gettext('Invalid file extension'))

        # Handle overwriting existing content
        if not self._is_uploaded_file(self.data):
            return

        if not self._allow_overwrite and self._check_exists(self.data.url):
            raise ValidationError(
                gettext('File "%s" already exists.' % self.data.filename)
            )

    def process(
            self, formdata, data=unset_value, extra_filters: list | None = None
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
                if self._is_file_uploaded(data):
                    self.data = data
                    break

    def populate_obj(self, obj: BaseAttachment, name: str):
        field = getattr(obj, name, None)
        if field:
            # If field should be deleted, clean it up
            if self._should_delete:
                setattr(obj, name, None)
                return

        if self._is_file_uploaded(self.data):
            setattr(
                obj, name,
                File(
                    content_type=self.data.content_type,
                    filename=self.data.filename,
                    content=self.data.stream
                )
            )

    @staticmethod
    def _check_exists(path: str):
        return op.exists(path) and op.isfile(path)
