import hashlib
import hmac
from datetime import datetime

import pytz

from goToVladi.core.utils import exceptions as exc
from goToVladi.core.utils.auth.models import UserTgAuth


def check_tg_auth(user: UserTgAuth, bot_token: str):
    data_check = user.to_tg_spec().encode("utf-8")
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    hmac_string = hmac.new(secret_key, data_check, hashlib.sha256).hexdigest()

    if hmac_string != user.hash:
        raise exc.InvalidCredentialsError

    utc_now = datetime.now(tz=pytz.UTC)
    if (utc_now - user.auth_date).seconds > 86400:
        raise exc.OutdatedCredentialsError
