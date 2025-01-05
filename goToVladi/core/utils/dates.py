from datetime import tzinfo, datetime

from dateutil import tz

DATE_FORMAT = r"%d.%m.%y"
DATE_FORMAT_USER = "ДД.ММ.ГГ"

TIME_FORMAT = r"%H:%M"
TIME_FORMAT_USER = "ЧЧ:ММ"

DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
DATETIME_FORMAT_USER = f"{DATE_FORMAT_USER} {TIME_FORMAT_USER}"

tz_utc = tz.gettz("UTC")
tz_local = tz.gettz("Asia/Vladivostok")


def get_now(_tz: tzinfo | None = None) -> datetime:
    return datetime.now().astimezone(tz=_tz or tz_local)


def get_now_isoformat(_tz: tzinfo | None = None):
    return get_now(_tz).isoformat()
