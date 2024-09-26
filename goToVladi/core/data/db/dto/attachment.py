from abc import ABC
from dataclasses import dataclass

from adaptix import Retort
from aiogram.enums import ContentType

file_retort = Retort()


@dataclass
class FileSchema:
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
    def from_dict(cls, data: dict) -> 'FileSchema':
        return file_retort.load(data, cls)


@dataclass
class BaseAttachment(ABC):
    id_: int
    content: FileSchema
    content_type: ContentType = ContentType.PHOTO

    @property
    def url(self):
        return self.content.url

    @property
    def path(self):
        return self.content.path
