__all__ = [
    "setup"
]

from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import Blueprint, Flask, Response
from pika.adapters.blocking_connection import BlockingChannel
from werkzeug.exceptions import InternalServerError

from goToVladi.flaskadmin.utils.exceptions import FlaskError


@inject
def internal_server_error(
        e: InternalServerError, mq: FromDishka[BlockingChannel]
):
    msg_ex = FlaskError(message=repr(e.original_exception))
    mq.basic_publish("logging", "log", str(msg_ex))
    return Response(status=500)


def setup(app: Flask):
    router = Blueprint("errors", __name__)

    app.register_error_handler(500, internal_server_error)

    return router
