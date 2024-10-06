__all__ = [
    "setup"
]

from flask import jsonify, abort, send_file, redirect, Response, Blueprint
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager

from goToVladi.flaskadmin.config.models.main import FlaskAppConfig


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


def setup(config: FlaskAppConfig):
    router = Blueprint(
        'media', __name__,
        url_prefix=config.admin.media_url
    )

    router.add_url_rule(
        '/<storage>/<file_id>',
        None,
        serve_media, methods=["GET"]
    )

    return router
