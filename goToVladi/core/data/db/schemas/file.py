from dataclasses import dataclass

from adaptix import Retort

file_retort = Retort()


@dataclass
class FileSchema:
    saved: bool
    filename: str
    content_type: str
    size: int
    files: list[str]
    width: int
    height: int
    file_id: str
    upload_storage: str
    uploaded_at: str
    path: str
    url: str
    saved: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'FileSchema':
        return file_retort.load(data, cls)
