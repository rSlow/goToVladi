from typing import Annotated

from fastapi import Path, APIRouter
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    RedirectResponse,
    StreamingResponse,
)
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager

from goToVladi.api import ApiAppConfig


async def serve_files(
        storage: Annotated[str, Path()],
        file_id: Annotated[str, Path()]
):
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")
        if isinstance(file.object.driver, LocalStorageDriver):
            """If file is stored in local storage, just return a
            FileResponse with the fill full path."""
            return FileResponse(
                file.get_cdn_url(), media_type=file.content_type,
                filename=file.filename
            )
        elif file.get_cdn_url() is not None:  # noqa: RET505
            """If file has public url, redirect to this url"""
            return RedirectResponse(file.get_cdn_url())
        else:
            """Otherwise, return a streaming response"""
            return StreamingResponse(
                file.object.as_stream(),
                media_type=file.content_type,
                headers={
                    "Content-Disposition": f"attachment;filename={file.filename}"
                },
            )
    except ObjectDoesNotExistError:
        return JSONResponse({"detail": "Not found"}, status_code=404)


def setup(config: ApiAppConfig):
    router = APIRouter(prefix=config.media.base_url)

    router.add_api_route(
        "/{storage}/{file_id}", serve_files,
        methods=["GET"], response_class=FileResponse
    )

    return router
