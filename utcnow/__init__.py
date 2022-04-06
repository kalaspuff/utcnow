from __future__ import annotations

import functools
import re
import sys
import time as time_
from datetime import datetime as datetime_
from datetime import timedelta as timedelta_
from datetime import timezone as timezone_
from datetime import tzinfo as tzinfo_
from decimal import Decimal
from numbers import Real
from typing import Any, Dict, Optional, Tuple, Type, Union, cast

from .__version_data__ import __version__, __version_info__

str_ = str

__author__: str_ = "Carl Oscar Aaro"
__email__: str_ = "hello@carloscar.com"

_SENTINEL = object()

_ACCEPTED_INPUT_FORMAT_VALUES = (
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M%z",
    "%Y-%m-%d %H:%M%z",
    "%Y-%m-%d%z",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)

NUMERIC_REGEX = re.compile(r"^[-]?([0-9]+|[.][0-9]+|[0-9]+[.]|[0-9]+[.][0-9]+)$")
PREFERRED_FORMAT_REGEX = re.compile(
    r"^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt ]([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9].[0-9]{6}([Zz]|[+-]00:00|)$"
)


utc = UTC = timezone_.utc


@functools.lru_cache(maxsize=128, typed=False)
def _is_numeric(value: str_) -> bool:
    if NUMERIC_REGEX.match(value):
        return True

    return False


@functools.lru_cache(maxsize=128, typed=True)
def _transform_value(value: Union[str_, datetime_, object, int, float, Decimal, Real]) -> str_:
    str_value: str_
    try:
        if isinstance(value, str_):
            str_value = value.strip()
        elif isinstance(value, (int, float)):
            return datetime_.utcfromtimestamp(value).isoformat(timespec="microseconds") + "Z"
        elif isinstance(value, (Decimal, Real)):
            str_value = datetime_.utcfromtimestamp(float(value)).isoformat(timespec="microseconds") + "Z"
        else:
            str_value = str_(value).strip()

        if (
            str_value
            and len(str_value) <= 21
            and "T" not in str_value
            and ":" not in str_value
            and "/" not in str_value
            and str_value.count("-") <= 1
            and _is_numeric(str_value)
        ):
            str_value = datetime_.utcfromtimestamp(float(str_value)).isoformat(timespec="microseconds") + "Z"
    except Exception:
        raise ValueError(f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats")

    if PREFERRED_FORMAT_REGEX.match(str_value):
        if int(str_value[8:10]) >= 30 or (int(str_value[5:7]) == 2 and int(str_value[8:10]) >= 28):
            try:
                dt_value = datetime_.strptime(str_value[0:10], "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats"
                )
        return (str_value[:10] + "T" + str_value[11:]).upper().rstrip("Z").rsplit("+00:00")[0].rsplit("-00:00")[0] + "Z"

    ends_with_utc = False
    if str_value.endswith(" UTC"):
        str_value = str_value[0:-4]
        ends_with_utc = True

    for format_ in _ACCEPTED_INPUT_FORMAT_VALUES:
        try:
            dt_value = datetime_.strptime(str_value, format_)
        except ValueError:
            continue

        if ends_with_utc and dt_value.tzinfo:
            raise ValueError(
                f"The input value '{value}' (type: {value.__class__}) uses double timezone declaration: 'UTC' and '{dt_value.tzinfo}'"
            )

        break
    else:
        raise ValueError(f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats")

    if not dt_value.tzinfo:
        # Timezone declaration missing, skipping tz application and blindly assuming UTC
        return dt_value.isoformat(timespec="microseconds") + "Z"

    return dt_value.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


@functools.lru_cache(maxsize=128)
def _timestamp_to_datetime(value: str_) -> datetime_:
    value = _transform_value(value)
    return datetime_.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")


@functools.lru_cache(maxsize=128)
def _timestamp_to_unixtime(value: str_) -> float:
    return _timestamp_to_datetime(value).timestamp()


@functools.lru_cache(maxsize=128)
def _timezone_from_string(value: str_) -> Optional[tzinfo_]:
    if value.upper() in (
        "UTC",
        "GMT",
        "UTC+0",
        "UTC-0",
        "GMT+0",
        "GMT-0",
        "Z",
        "ZULU",
        "00:00",
        "+00:00",
        "-00:00",
        "0000",
        "+0000",
        "-0000",
    ):
        return UTC

    if value and value[0] in ("+", "-"):
        m = re.match(r"^[+-]([0-9]{2}):?([0-9]{2})$", value)
        if not m:
            return None

        modifier = 1 if value[0] == "+" else -1

        td = timedelta_(hours=int(m.group(1)), minutes=int(m.group(2)))
        if td.days == 1 and td == timedelta_(days=1):
            td = timedelta_(days=1, microseconds=-1)

        return timezone_(modifier * td)

    return None


class _metaclass(type):
    def __new__(cls: Type[_metaclass], name: str_, bases: Tuple[type, ...], attributedict: Dict) -> _metaclass:
        result = cast(Type["_baseclass"], super().__new__(cls, name, bases, dict(attributedict)))

        return result


class _baseclass(metaclass=_metaclass):
    def __init__(self) -> None:
        pass

    def __call__(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> str_:
        if value is _SENTINEL:
            return datetime_.utcnow().isoformat(timespec="microseconds") + "Z"
        return _transform_value(value)


class now_(_baseclass):
    def __new__(cls, *args: Any) -> now_:
        result = object.__new__(cls, *args)

        return result

    def __str__(self) -> str_:
        return datetime_.utcnow().isoformat(timespec="microseconds") + "Z"

    def __repr__(self) -> str_:
        return datetime_.utcnow().isoformat(timespec="microseconds") + "Z"


class utcnow_(_baseclass):
    now = now_()

    def __new__(cls, *args: Any) -> utcnow_:
        result = object.__new__(cls, *args)

        return result

    def as_string(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> str_:
        if value is _SENTINEL:
            return datetime_.utcnow().isoformat(timespec="microseconds") + "Z"
        return _transform_value(value)

    def as_datetime(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> datetime_:
        if value is _SENTINEL:
            # 'datetime.datetime.now(UTC)' is faster than 'datetime.datetime.utcnow().replace(tzinfo=UTC)'
            return datetime_.now(UTC)
        return _timestamp_to_datetime(value)

    def as_unixtime(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> float:
        if value is _SENTINEL:
            return time_.time()
        return _timestamp_to_unixtime(value)

    def timediff(
        self,
        begin: Union[str_, datetime_, object, int, float, Decimal, Real],
        end: Union[str_, datetime_, object, int, float, Decimal, Real],
        unit: str_ = "seconds",
    ) -> float:
        delta = _timestamp_to_datetime(end) - _timestamp_to_datetime(begin)
        unit = unit.lower()

        if unit in ("seconds", "second", "sec", "s"):
            return delta.total_seconds()
        if unit in ("minutes", "minute", "min", "m"):
            return delta.total_seconds() / 60
        if unit in ("hours", "hour", "h"):
            return delta.total_seconds() / 3600
        if unit in ("days", "day", "d"):
            return delta.total_seconds() / 86400
        if unit in ("weeks", "week", "w"):
            return delta.total_seconds() / (86400 * 7)

        raise ValueError(f"Unknown unit '{unit}' for utcnow.timediff")

    def as_date_string(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        tz: Optional[Union[str_, tzinfo_]] = None,
    ) -> str_:
        date_tz: Optional[tzinfo_] = None

        if not tz:
            date_tz = UTC
        elif isinstance(tz, tzinfo_):
            date_tz = tz
        elif isinstance(tz, str_):
            date_tz = _timezone_from_string(tz)

        if not date_tz:
            raise ValueError(
                f"Unknown timezone value '{tz}' (type: {tz.__class__.__name__}) - use value of type 'datetime.tzinfo' or an utcoffset string value"
            )

        if value is _SENTINEL:
            return datetime_.now(date_tz).date().isoformat()

        return _timestamp_to_datetime(value).astimezone(date_tz).date().isoformat()

    as_str = as_string
    as_rfc3339 = as_string
    to_string = as_string
    to_str = as_string
    to_rfc3339 = as_string
    get_string = as_string
    get_str = as_string
    get_rfc3339 = as_string
    get = as_string
    string = as_string
    str = as_string
    rfc3339 = as_string
    timestamp_rfc3339 = as_string
    ts_rfc3339 = as_string
    rfc3339_timestamp = as_string
    rfc3339_ts = as_string
    utcnow_rfc3339 = as_string
    rfc3339_utcnow = as_string
    now_rfc3339 = as_string
    rfc3339_now = as_string
    get_now = as_string

    as_date = as_datetime
    as_dt = as_datetime
    to_datetime = as_datetime
    to_date = as_datetime
    to_dt = as_datetime
    get_datetime = as_datetime
    get_date = as_datetime
    get_dt = as_datetime
    datetime = as_datetime
    date = as_datetime
    dt = as_datetime

    as_unix = as_unixtime
    as_time = as_unixtime
    as_timestamp = as_unixtime
    as_ut = as_unixtime
    as_ts = as_unixtime
    as_float = as_unixtime
    to_unixtime = as_unixtime
    to_unix = as_unixtime
    to_time = as_unixtime
    to_timestamp = as_unixtime
    to_ut = as_unixtime
    to_ts = as_unixtime
    to_float = as_unixtime
    get_unixtime = as_unixtime
    get_unix = as_unixtime
    get_time = as_unixtime
    get_timestamp = as_unixtime
    get_ut = as_unixtime
    get_ts = as_unixtime
    get_float = as_unixtime
    unixtime = as_unixtime
    unix = as_unixtime
    time = as_unixtime
    timestamp = as_unixtime
    ut = as_unixtime
    ts = as_unixtime

    time_diff = timediff
    diff = timediff
    timedelta = timediff
    delta = timediff

    as_datestring = as_date_string
    as_date_str = as_date_string
    as_datestr = as_date_string
    to_date_string = as_date_string
    to_datestring = as_date_string
    to_date_str = as_date_string
    to_datestr = as_date_string
    get_date_string = as_date_string
    get_datestring = as_date_string
    get_datestr = as_date_string
    get_date_string = as_date_string
    get_today = as_date_string
    get_today_date = as_date_string
    get_todays_date = as_date_string
    get_date_today = as_date_string
    date_today = as_date_string
    today_date = as_date_string
    todays_date = as_date_string
    today = as_date_string
    date_string = as_date_string
    datestring = as_date_string
    date_str = as_date_string
    datestr = as_date_string

    def __str__(self) -> str_:
        return self.as_string()

    def __repr__(self) -> str_:
        return self.as_string()


class _module(utcnow_):
    __version__: str_ = __version__  # noqa
    __version_info__: Tuple[Union[int, str_], ...] = __version_info__
    __author__: str_ = __author__
    __email__: str_ = __email__

    utcnow = utcnow_()

    def __new__(cls, *args: Any) -> _module:
        result = object.__new__(cls, *args)

        setattr(result, "now", result.utcnow)

        return result


_module_value = _module()
utcnow = _module_value.utcnow
now = utcnow

as_string = _module_value.as_string
as_str = as_string
as_rfc3339 = as_string
to_string = as_string
to_str = as_string
to_rfc3339 = as_string
get_string = as_string
get_str = as_string
get_rfc3339 = as_string
get = as_string
string = as_string
str = as_string
rfc3339 = as_string
timestamp_rfc3339 = as_string
ts_rfc3339 = as_string
rfc3339_timestamp = as_string
rfc3339_ts = as_string
utcnow_rfc3339 = as_string
rfc3339_utcnow = as_string
now_rfc3339 = as_string
rfc3339_now = as_string
get_now = as_string

as_datetime = _module_value.as_datetime
as_date = as_datetime
as_dt = as_datetime
to_datetime = as_datetime
to_date = as_datetime
to_dt = as_datetime
get_datetime = as_datetime
get_date = as_datetime
get_dt = as_datetime
datetime = as_datetime
date = as_datetime
dt = as_datetime

as_unixtime = _module_value.as_unixtime
as_unix = as_unixtime
as_time = as_unixtime
as_timestamp = as_unixtime
as_ut = as_unixtime
as_ts = as_unixtime
as_float = as_unixtime
to_unixtime = as_unixtime
to_unix = as_unixtime
to_time = as_unixtime
to_timestamp = as_unixtime
to_ut = as_unixtime
to_ts = as_unixtime
to_float = as_unixtime
get_unixtime = as_unixtime
get_unix = as_unixtime
get_time = as_unixtime
get_timestamp = as_unixtime
get_ut = as_unixtime
get_ts = as_unixtime
get_float = as_unixtime
unixtime = as_unixtime
unix = as_unixtime
time = as_unixtime
timestamp = as_unixtime
ut = as_unixtime
ts = as_unixtime

timediff = _module_value.timediff
time_diff = timediff
diff = timediff
timedelta = timediff
delta = timediff

as_date_string = _module_value.as_date_string
as_datestring = as_date_string
as_date_str = as_date_string
as_datestr = as_date_string
to_date_string = as_date_string
to_datestring = as_date_string
to_date_str = as_date_string
to_datestr = as_date_string
get_date_string = as_date_string
get_datestring = as_date_string
get_date_str = as_date_string
get_datestr = as_date_string
get_today = as_date_string
get_today_date = as_date_string
get_todays_date = as_date_string
get_date_today = as_date_string
date_today = as_date_string
today_date = as_date_string
todays_date = as_date_string
today = as_date_string
date_string = as_date_string
datestring = as_date_string
date_str = as_date_string
datestr = as_date_string


__all__ = [
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "utcnow",
    "now",
    "as_string",
    "as_str",
    "as_rfc3339",
    "to_string",
    "to_str",
    "to_rfc3339",
    "get_string",
    "get_str",
    "get_rfc3339",
    "get",
    "string",
    "str",
    "rfc3339",
    "timestamp_rfc3339",
    "ts_rfc3339",
    "rfc3339_timestamp",
    "rfc3339_ts",
    "utcnow_rfc3339",
    "rfc3339_utcnow",
    "now_rfc3339",
    "rfc3339_now",
    "get_now",
    "as_datetime",
    "as_date",
    "as_dt",
    "to_datetime",
    "to_date",
    "to_dt",
    "get_datetime",
    "get_date",
    "get_dt",
    "datetime",
    "date",
    "dt",
    "as_unixtime",
    "as_unix",
    "as_time",
    "as_timestamp",
    "as_ut",
    "as_ts",
    "as_float",
    "to_unixtime",
    "to_unix",
    "to_time",
    "to_timestamp",
    "to_ut",
    "to_ts",
    "to_float",
    "get_unixtime",
    "get_unix",
    "get_time",
    "get_timestamp",
    "get_ut",
    "get_ts",
    "get_float",
    "unixtime",
    "unix",
    "time",
    "timestamp",
    "ut",
    "ts",
    "timediff",
    "time_diff",
    "diff",
    "timedelta",
    "delta",
    "as_date_string",
    "as_datestring",
    "as_date_str",
    "as_datestr",
    "to_date_string",
    "to_datestring",
    "to_date_str",
    "to_datestr",
    "get_date_string",
    "get_datestring",
    "get_date_str",
    "get_datestr",
    "get_today",
    "get_today_date",
    "get_todays_date",
    "get_date_today",
    "date_today",
    "today_date",
    "todays_date",
    "today",
    "date_string",
    "datestring",
    "date_str",
    "datestr",
]

_actual_module = sys.modules[__name__]  # noqa

_module_value.__spec__ = _actual_module.__spec__  # type: ignore
_module_value.__path__ = _actual_module.__path__  # type: ignore
_module_value.__all__ = _actual_module.__all__  # type: ignore
_module_value.__cached__ = _actual_module.__cached__  # type: ignore
_module_value.__dict__ = _actual_module.__dict__
_module_value.__doc__ = _actual_module.__doc__
_module_value.__file__ = _actual_module.__file__  # type: ignore
_module_value.__name__ = _actual_module.__name__  # type: ignore
_module_value.__package__ = _actual_module.__package__  # type: ignore

sys.modules[__name__] = _module_value  # type: ignore
