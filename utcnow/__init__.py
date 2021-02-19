from __future__ import annotations

import sys
from datetime import datetime as datetime_
from datetime import timezone as timezone_
from typing import Any, Dict, Tuple, Type, Union, cast

from .__version_data__ import __version__, __version_info__

str_ = str

__author__: str_ = "Carl Oscar Aaro"
__email__: str_ = "hello@carloscar.com"

_SENTINEL = object()

_ACCEPTED_INPUT_FORMAT_VALUES = (
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%dT%H:%M%z",
    "%Y-%m-%d %H:%M%z",
    "%Y-%m-%d%z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)


def _transform_value(value: Union[str_, datetime_, object] = _SENTINEL) -> str_:
    if value is _SENTINEL:
        return datetime_.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    if not isinstance(value, str_):
        str_value = str_(value)
    else:
        str_value = value

    str_value = str_value.strip()

    ends_with_utc = False
    if str_value.endswith(" UTC"):
        str_value = str_value[0:-4]
        ends_with_utc = True

    dt_value = None
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

    if not dt_value:
        raise ValueError(f"Input value '{value}' (type: {value.__class__}) does not match allowed input format")

    if not dt_value.tzinfo:
        # Timezone declaration missing, skipping tz application and blindly assuming UTC
        return dt_value.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    return dt_value.astimezone(timezone_.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


class _metaclass(type):
    def __new__(cls: Type[_metaclass], name: str_, bases: Tuple[type, ...], attributedict: Dict) -> _metaclass:
        result = cast(Type["_baseclass"], super().__new__(cls, name, bases, dict(attributedict)))

        return result


class _baseclass(metaclass=_metaclass):
    def __init__(self) -> None:
        pass

    def __call__(self, value: Union[str_, datetime_, object] = _SENTINEL) -> str_:
        return _transform_value(value)


class utcnow_(_baseclass):
    def __new__(cls, *args: Any) -> utcnow_:
        result = cast(utcnow_, object.__new__(cls, *args))

        return result

    def as_string(self, value: Union[str_, datetime_, object] = _SENTINEL) -> str_:
        return _transform_value(value)

    as_str = as_string
    to_string = as_string
    to_str = as_string
    string = as_string
    str = as_string

    def as_datetime(self, value: Union[str_, datetime_, object] = _SENTINEL) -> datetime_:
        return datetime_.strptime(_transform_value(value), "%Y-%m-%dT%H:%M:%S.%f%z")

    as_date = as_datetime
    to_datetime = as_datetime
    to_date = as_datetime
    datetime = as_datetime
    date = as_datetime

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
        result = cast(_module, object.__new__(cls, *args))

        return result


_module_value = _module()
utcnow = _module_value.utcnow

as_string = _module_value.as_string
as_str = as_string
to_string = as_string
to_str = as_string
string = as_string
str = as_string

as_datetime = _module_value.as_datetime
as_date = as_datetime
to_datetime = as_datetime
to_date = as_datetime
datetime = as_datetime
date = as_datetime

__all__ = [
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "utcnow",
    "as_string",
    "as_str",
    "string",
    "str",
    "as_datetime",
    "as_date",
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
