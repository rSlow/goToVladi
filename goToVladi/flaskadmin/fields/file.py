import os.path as op

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


class SQLAlchemyFileUploadInput:
    empty_template = '<input %(file)s>'
    input_type = 'file'
    file_template = (
        "<div> "
        "  <a %(a)s>%(url)s</a>"  # TODO mount static endpoint 
        "</div>"
        "<input %(file)s>"
    )

    def __call__(self, field: FileUploadField, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        template = self.file_template if field.data else self.empty_template
        if field.errors:
            template = self.empty_template

        value = field.data or ""
        if isinstance(value, File):
            url = value.path
        else:
            url = ""

        args = {
            "text": html_params(
                type="text", readonly="readonly", value=value,
                name=field.name
            ),
            "file": html_params(type="file", value=value, **kwargs),
            "marker": '_%s-delete' % field.name,
            "a": html_params(href=f"/static/{url}"),
            "url": url
        }
        return Markup(template % args)


class SQLAlchemyFileUploadField(FileUploadField):
    widget = SQLAlchemyFileUploadInput()
    data: FileStorage | None

    def __init__(
            self, label=None, validators=None, base_path=None,
            relative_path=None, namegen=None, allowed_extensions=None,
            permission=0o666, allow_overwrite=True, **kwargs
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

    @staticmethod
    def __is_uploaded_file(data: FileStorage):
        if data:
            return any((
                isinstance(data, FileStorage) and data.filename,
                isinstance(data, File) and not data["saved"]
            ))

    def pre_validate(self, form: BaseForm):
        if all((
                self.__is_uploaded_file(self.data),
                not self.is_file_allowed(self.data.filename)
        )):
            raise ValidationError(gettext('Invalid file extension'))

        # Handle overwriting existing content
        if not self.__is_uploaded_file(self.data):
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
                if self.__is_uploaded_file(data):
                    self.data = data
                    break

    def populate_obj(self, obj: BaseAttachment, name: str):
        field = getattr(obj, name, None)
        if field:
            # If field should be deleted, clean it up
            if self._should_delete:
                setattr(obj, name, None)
                return

        if self.__is_uploaded_file(self.data):
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
