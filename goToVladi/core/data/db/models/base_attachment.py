from abc import abstractmethod
from typing import TypeVar

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_file import FileField

from goToVladi.core.data.db import dto

AttachmentDtoType = TypeVar(
    "AttachmentDtoType", bound=dto.BaseAttachment,
    covariant=True, contravariant=False
)


class BaseAttachment:
    content_type: Mapped[str]
    content = mapped_column(FileField)

    # need to set ForeignKey attribute in subclass
    # model_id: Mapped[int] = mapped_column(ForeignKey('model.id'))

    def convert_content(self) -> dto.FileSchema:
        return dto.FileSchema.from_dict(self.content)

    @abstractmethod
    def to_dto(self) -> AttachmentDtoType:
        ...
