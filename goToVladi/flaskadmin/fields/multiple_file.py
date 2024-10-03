from sqlalchemy_file import File
from werkzeug.datastructures import FileStorage
from wtforms.fields import MultipleFileField

from goToVladi.core.data.db.dao.base import ModelType
from goToVladi.core.data.db.models.base_attachment import BaseAttachment


class SQLAlchemyMultipleFileUploadField(MultipleFileField):
    data: list[FileStorage]

    def __init__(
            self,
            field_name: str, relation_class: type[BaseAttachment],
            **kwargs
    ):
        super().__init__(**kwargs)
        self.field_name = field_name
        self.relation_class = relation_class

    def populate_obj(self, obj: ModelType, _):
        if any([
            not self.data,
            len(self.data) == 1 and self.data[0].content_length == 0
        ]):
            return

        if not hasattr(obj, self.field_name):
            raise AttributeError(
                f"Object {obj.__class__.__name__} "
                f"does not have field {self.field_name}."
            )
        data_list = getattr(obj, self.field_name, [])
        for form_file in self.data:
            data_list.append(
                self.relation_class(
                    content=File(
                        content_type=form_file.content_type,
                        filename=form_file.filename,
                        content=form_file.stream
                    )
                )
            )
        setattr(obj, self.field_name, data_list)
