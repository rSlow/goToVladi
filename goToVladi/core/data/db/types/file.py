import os.path as op
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy_file import File as BaseFile
from sqlalchemy_file.stored_file import StoredFile


class File(BaseFile):
    def store_content(
            self,
            content: Any,
            upload_storage: Optional[str] = None,
            name: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None,
            extra: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            content_path: Optional[str] = None,
    ) -> StoredFile:
        file_ext = op.splitext(self["filename"])[1]
        name = name or f"{str(uuid4())}" + file_ext
        return super().store_content(
            content=content,
            upload_storage=upload_storage,
            name=name,
            metadata=metadata,
            extra=extra,
            headers=headers,
            content_path=content_path,
        )
