from datetime import tzinfo, datetime

from dateutil import tz

tz_utc = tz.gettz("UTC")
tz_local = tz.gettz("Asia/Vladivostok")


def get_now(_tz: tzinfo | None = None) -> datetime:
    return datetime.now().astimezone(tz=_tz or tz_local)


def get_now_isoformat(_tz: tzinfo | None = None):
    return get_now(_tz).isoformat()
