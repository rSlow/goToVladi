from .config import ApiConfigProvider
from .auth import AuthProvider


def get_api_providers():
    return [
        ApiConfigProvider(),
        AuthProvider()
    ]
