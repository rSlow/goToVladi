from flask_admin.form import FileUploadField
from markupsafe import Markup
from wtforms.widgets import html_params


class SQLAlchemyFileUploadInput:
    input_type = 'file'
    empty_template = (
        "<div class='input-container'>"
        "  <input %(file)s>"
        "  <label %(label)s>"
        "    %(label_text)s"
        "  </label>"
        "</div>"
    )
    data_template = (
            "<div>"
            " <input %(text)s>"
            " <input type='checkbox' name='%(marker)s'>Delete</input>"
            "</div>" + empty_template
    )

    def __init__(self, multiple: bool = False):
        super().__init__()
        self.multiple = multiple

    def _get_base_args(self, field: FileUploadField, **kwargs) -> dict:
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        value = field.data or ""
        return {
            "text": html_params(
                type="text", readonly="readonly", value=value,
                name=field.name
            ),
            "file": html_params(
                type="file", value=value,
                hidden="True",
                **kwargs
            ),
            "marker": '_%s-delete' % field.name,
            "label_text": "Выбрать файл" + self.multiple * "ы",
            "label": html_params(**{
                "for": field.id,
                "class": "file-upload-label",
            })
        }

    def verify_template(self, field: FileUploadField, template: str):
        template = template if field.data else self.empty_template
        if field.errors:
            template = self.empty_template
        return template

    def __call__(self, field: FileUploadField, **kwargs):
        template = self.verify_template(field, self.data_template)
        if self.multiple:
            kwargs["multiple"] = True
        args = self._get_base_args(field, **kwargs)
        return Markup(template % args)


class SQLAlchemyFileUploadField(FileUploadField):
    widget = SQLAlchemyFileUploadInput()
