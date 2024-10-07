from flask_admin.form import FileUploadField, FileUploadInput


class SQLAlchemyFileUploadInput(FileUploadInput):
    def __init__(self, multiple: bool = True):
        super().__init__()
        self.multiple = multiple

    empty_template = (
        "<div class='input-wrapper'>"
        "  <input %(file)s>"
        "</div>"
    )
    data_template = (
            "<div>"
            " <input %(text)s>"
            " <input type='checkbox' name='%(marker)s'>Delete</input>"
            "</div>" + empty_template
    )

    def __call__(self, *args, **kwargs):
        if self.multiple:
            kwargs["multiple"] = True
        return super().__call__(*args, **kwargs)


class SQLAlchemyFileUploadField(FileUploadField):
    widget = SQLAlchemyFileUploadInput()
