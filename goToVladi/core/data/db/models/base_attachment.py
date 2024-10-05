from abc import abstractmethod
from typing import TypeVar

from sqlalchemy.orm import MappedColumn
from sqlalchemy_file import FileField

from goToVladi.core.data.db import dto

AttachmentDtoType = TypeVar(
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

    @abstractmethod
    def to_dto(self) -> AttachmentDtoType:
        ...
