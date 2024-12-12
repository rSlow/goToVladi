__all__ = [
    "setup"
]

from dishka import FromDishka
from dishka.integrations.flask import inject
from flask import Blueprint, Flask, Response
from pika.adapters.blocking_connection import BlockingChannel
from werkzeug.exceptions import InternalServerError

from goToVladi.flaskadmin.utils.exceptions import FlaskError


def create_error_handler(status: int):
    @inject
    def _error_route(e: InternalServerError, mq: FromDishka[BlockingChannel]):
        msg_ex = FlaskError(message=repr(e.original_exception))
        mq.basic_publish("logging", "log", str(msg_ex))
        return Response(status=status)

    return _error_route


def setup(app: Flask):
    router = Blueprint("errors", __name__)

    app.register_error_handler(500, create_error_handler(500))
    app.register_error_handler(501, create_error_handler(501))
    app.register_error_handler(502, create_error_handler(502))

    return router
