from flask import jsonify, abort, send_file, redirect, stream_with_context, \
    Response
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager


async def serve_files(storage: str, file_id: str):
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")
        if isinstance(file.object.driver, LocalStorageDriver):
            """If file is stored in local storage, just return a
            FileResponse with the fill full path."""
            return send_file(
                file.get_cdn_url(),
                mimetype=file.content_type, download_name=file.filename
            )
        elif file.get_cdn_url() is not None:  # noqa: RET505
            """If file has public url, redirect to this url"""
            return redirect(file.get_cdn_url())
        else:
            """Otherwise, return a streaming response"""
            return Response(stream_with_context(file.object.as_stream))

    except ObjectDoesNotExistError:
        return abort(404, jsonify({"detail": "Not found"}))
