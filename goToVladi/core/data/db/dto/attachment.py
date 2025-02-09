from typing import TypeVar

from pydantic import BaseModel

from goToVladi.core.data.db.dto.mixins import ORMMixin


class FileSchema(BaseModel):
    filename: str
    content_type: str
    size: int
    files: list[str]
    file_id: str
    upload_storage: str
    uploaded_at: str
    path: str
    url: str
    saved: bool

    @classmethod
    def from_dict(cls, data: dict):
        return cls.model_validate(data)


class BaseAttachment(BaseModel, ORMMixin):
    _id: int
    content: FileSchema

    @property
    def url(self):
        return self.content.url

    @property
    def path(self):
        return self.content.path

    def to_dto(self):  # can't do this method abstract because of dataclass :(
        raise NotImplementedError


AttachmentType = TypeVar(
    "AttachmentType", bound=type[BaseAttachment],
    covariant=True, contravariant=False
)
