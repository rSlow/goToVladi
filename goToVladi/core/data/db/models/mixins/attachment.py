import typing as t
from pathlib import Path

from sqlalchemy.orm import mapped_column, declared_attr
from sqlalchemy_file import FileField
from sqlalchemy_file.validators import SizeValidator

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.types.file import File
from goToVladi.core.data.db.utils import file_field
from goToVladi.core.utils.functools import get_generic_types

AttachmentDtoType = t.TypeVar(
    "AttachmentDtoType", bound=dto.BaseAttachment,
    covariant=True, contravariant=False
)


class AttachmentProtocol(t.Generic[AttachmentDtoType]):
    __upload_type__ = File

    def __init__(self, *args, **kwargs) -> None:
        self.__model_dto: type[AttachmentDtoType] = get_generic_types(type(self), 0)[0]
        super().__init__(*args, **kwargs)

    @declared_attr
    def content(self):
        return mapped_column(
            FileField(
                validators=[SizeValidator(max_size="50M")],
                upload_type=self.__upload_type__
            )
        )

    """
    
    here you need to set ForeignKey and relationship attribute in subclass
    
    <parent_model>_id: Mapped[int] = mapped_column(ForeignKey('<model>.id'))
    <parent_model> = relationship("<Parent>", back_populates="medias", uselist=False)
     
    """

    def convert_content(self) -> dto.FileSchema:
        return dto.FileSchema.from_dict(self.content)

    def get_file_path(self, media_path: Path):
        content = self.convert_content()
        relative_path = file_field.get_relative_path(content.url, media_path)
        return relative_path

    def to_dto(self) -> dto.DeliveryMedia:
        return self.__model_dto.model_validate(self, context={"content": self.convert_content()})
