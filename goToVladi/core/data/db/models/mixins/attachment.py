import typing as t
from abc import abstractmethod
from pathlib import Path

from sqlalchemy.orm import mapped_column, declared_attr
from sqlalchemy_file import FileField
from sqlalchemy_file.validators import SizeValidator

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.types.file import File
from goToVladi.core.data.db.utils import file_field

AttachmentDtoType = t.TypeVar(
    "AttachmentDtoType", bound=dto.BaseAttachment,
    covariant=True, contravariant=False
)


class AttachmentProtocol:
    __upload_type__ = File

    __storage_name__: str

    # need to set __storage_name__ field with specifying the storage
    # __storage_name__ = "storage_name"

    @declared_attr
    def content(self):
        return mapped_column(
            FileField(
                upload_storage=self.__storage_name__,
                validators=[SizeValidator(max_size="50M")],
                upload_type=self.__upload_type__
            )
        )

    # need to set ForeignKey and relationship attribute in subclass
    # parent_model_id: Mapped[int] = mapped_column(ForeignKey('model.id'))
    # parent_model = relationship(
    #     "Parent", back_populates="medias", uselist=False
    # )

    def convert_content(self) -> dto.FileSchema:
        return dto.FileSchema.from_dict(self.content)

    def get_file_path(self, media_path: Path):
        content = self.convert_content()
        relative_path = file_field.get_relative_path(content.url, media_path)
        return relative_path

    @abstractmethod
    def to_dto(self) -> AttachmentDtoType:
        ...
