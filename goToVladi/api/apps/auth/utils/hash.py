import hashlib
import hmac

from aiogram.utils.web_app import check_webapp_signature, \
    parse_webapp_init_data, WebAppInitData
from fastapi import HTTPException, status

from goToVladi.api.apps.auth.models import UserTgAuth


def check_tg_hash(user: UserTgAuth, bot_token: str):
    data_check = user.to_tg_spec().encode("utf-8")
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    hmac_string = hmac.new(secret_key, data_check, hashlib.sha256).hexdigest()
    if hmac_string != user.hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="something wrong"
        )


def check_webapp_hash(data: str, bot_token: str) -> WebAppInitData:
    if not check_webapp_signature(bot_token, data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="tg hash mismatch"
        )
    return parse_webapp_init_data(data)
