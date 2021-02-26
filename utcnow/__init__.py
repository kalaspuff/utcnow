from __future__ import annotations

import functools
import re
import sys
from datetime import datetime as datetime_
from datetime import timezone as timezone_
from decimal import Decimal
from numbers import Real
from typing import Any, Dict, Tuple, Type, Union, cast

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
        raise ValueError(f"Input value '{value}' (type: {value.__class__}) does not match allowed input format")

    if PREFERRED_FORMAT_REGEX.match(str_value):
        if int(str_value[8:10]) >= 30 or (int(str_value[5:7]) == 2 and int(str_value[8:10]) >= 28):
            try:
                dt_value = datetime_.strptime(str_value[0:10], "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Input value '{value}' (type: {value.__class__}) does not match allowed input format")
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
                f"Input value '{value}' (type: {value.__class__}) uses double timezone declaration: 'UTC' and '{dt_value.tzinfo}'"
            )

        break
    else:
        raise ValueError(f"Input value '{value}' (type: {value.__class__}) does not match allowed input format")

    if not dt_value.tzinfo:
        # Timezone declaration missing, skipping tz application and blindly assuming UTC
        return dt_value.isoformat(timespec="microseconds") + "Z"

    return dt_value.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


@functools.lru_cache(maxsize=128)
def _timestamp_to_datetime(value: str_) -> datetime_:
    return datetime_.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")


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


class utcnow_(_baseclass):
    def __new__(cls, *args: Any) -> utcnow_:
        result = cast(utcnow_, object.__new__(cls, *args))

        return result

    def as_string(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> str_:
        if value is _SENTINEL:
            return datetime_.utcnow().isoformat(timespec="microseconds") + "Z"
        return _transform_value(value)

    as_str = as_string
    as_timestamp = as_string
    to_string = as_string
    to_str = as_string
    to_timestamp = as_string
    get_string = as_string
    get_str = as_string
    get_timestamp = as_string
    get = as_string
    string = as_string
    str = as_string

    def as_datetime(self, value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL) -> datetime_:
        if value is _SENTINEL:
            # return datetime_.utcnow().replace(tzinfo=UTC)
            return datetime_.now(UTC)
        return _timestamp_to_datetime(_transform_value(value))

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
    now = utcnow_()

    def __new__(cls, *args: Any) -> _module:
        result = cast(_module, object.__new__(cls, *args))

        return result


_module_value = _module()
utcnow = _module_value.utcnow
now = _module_value.now

as_string = _module_value.as_string
as_str = as_string
as_timestamp = as_string
to_string = as_string
to_str = as_string
to_timestamp = as_string
get_string = as_string
get_str = as_string
get_timestamp = as_string
get = as_string
string = as_string
str = as_string

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

__all__ = [
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "utcnow",
    "now",
    "as_string",
    "as_str",
    "as_timestamp",
    "to_string",
    "to_str",
    "to_timestamp",
    "get_string",
    "get_str",
    "get_timestamp",
    "string",
    "str",
    "as_datetime",
    "as_date",
    "to_datetime",
    "to_date",
    "get_datetime",
    "get_date",
    "datetime",
    "date",
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
