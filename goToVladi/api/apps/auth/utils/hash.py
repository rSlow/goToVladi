from aiogram.utils.web_app import check_webapp_signature, \
    parse_webapp_init_data, WebAppInitData
from fastapi import HTTPException, status

from goToVladi.core.utils.auth.hash import check_tg_auth as base_check_tg_hash
from goToVladi.core.utils.auth.models import UserTgAuth


def check_tg_hash(user: UserTgAuth, bot_token: str):
    if not base_check_tg_hash(user, bot_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="something wrong"
        )


def check_webapp_hash(data: str, bot_token: str) -> WebAppInitData:
    if not check_webapp_signature(bot_token, data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="tg hash mismatch"
        )
    return parse_webapp_init_data(data)
