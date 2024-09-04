from fastapi import APIRouter
from starlette.responses import HTMLResponse


def setup():
    router = APIRouter(prefix='/auth', tags=['auth'])

    router.add_api_route("/token", login, methods=["POST"])
    router.add_api_route("/login", tg_login_page, response_class=HTMLResponse, methods=["GET"])
    router.add_api_route("/logout", logout, methods=["POST"])
    router.add_api_route("/login/data", tg_login_result, methods=["GET"])
    router.add_api_route("/login/data", tg_login_result_post, methods=["POST"])
    router.add_api_route("/login/webapp", webapp_login_result_post, methods=["POST"])

    return router
