from flask import jsonify, abort, send_file, redirect, Response
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager


async def serve_media(storage: str, file_id: str):
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")
        if isinstance(file.object.driver, LocalStorageDriver):
            """If file is stored in local storage, just return a
            FileResponse with the fill full path."""
            return send_file(
                file.get_cdn_url(),
                mimetype=file.content_type, download_name=file.filename
            )
        elif file.get_cdn_url() is not None:
            """If file has public url, redirect to this url"""
            return redirect(file.get_cdn_url())
        else:
            """Otherwise, return a streaming response"""
            return Response(
                file.object.as_stream(),
                mimetype=file.content_type,
                headers={
                    "Content-Disposition": f"attachment;"
                                           f"filename={file.filename}"
                },
            )

    except ObjectDoesNotExistError:
        return abort(404, jsonify({"detail": "File not found"}))
