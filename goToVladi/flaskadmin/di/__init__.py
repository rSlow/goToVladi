from .auth import AuthProvider
from .config import FlaskProvider
from .db import SyncDbProvider
from .mq import SyncMQProvider


def get_flask_providers():
    return [
        FlaskProvider(),
        SyncDbProvider(),
        SyncMQProvider(),
        AuthProvider(),
    ]
