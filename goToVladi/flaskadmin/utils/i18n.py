from flask import Flask
from flask import g, request
from flask_babel import Babel


def get_locale():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(["ru", "en"])


def setup(app: Flask):
    babel = Babel()
    babel.init_app(app, locale_selector=get_locale)
