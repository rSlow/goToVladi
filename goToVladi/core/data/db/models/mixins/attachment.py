import typing as t
from abc import abstractmethod
from pathlib import Path

from sqlalchemy.orm import MappedColumn
from sqlalchemy_file import FileField

from goToVladi.core.data.db import dto
from goToVladi.core.data.db.utils import file_field

AttachmentDtoType = t.TypeVar(
    "AttachmentDtoType", bound=dto.BaseAttachment,
    covariant=True, contravariant=False
)


class AttachmentProtocol:
    content: MappedColumn[FileField]  # abstract

    # need to set ForeignKey and relationship attribute in subclass
    # parent_model_id: Mapped[int] = mapped_column(ForeignKey('model.id'))
    # parent_model = relationship(
    #     "Parent", back_populates="medias", uselist=False
    # )
    # need to set content field with specifying the storage
    # content = mapped_column(FileField(upload_storage="storage_name"))

    def convert_content(self) -> dto.FileSchema:
        return dto.FileSchema.from_dict(self.content)

    def get_file_path(self, media_path: Path):
        content = self.convert_content()
        relative_path = file_field.get_relative_path(content.url, media_path)
        return relative_path

    @abstractmethod
    def to_dto(self) -> AttachmentDtoType:
        ...
