from goToVladi.api.di.config import ApiConfigProvider


def get_api_providers():
    return [
        ApiConfigProvider(),
    ]
