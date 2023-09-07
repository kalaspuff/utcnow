"""
Timestamps as RFC 3339 (Date & Time on the Internet) formatted strings with conversion functionality from other
timestamp formats or for timestamps on other timezones. Additionally converts timestamps from datetime objets
and other common date utilities.

``utcnow.rfc3339_timestamp(value, modifier)``
    Transforms the input value to a timestamp string in RFC3339 format.
``utcnow.as_datetime(value, modifier)``
    Transforms the input value to a datetime object.
``utcnow.as_unixtime(value, modifier)``
    Transforms the input value to a float value representing unixtime.
``utcnow.as_protobuf(value, modifier)``
    Transforms the input value to a google.protobuf.Timestamp message.

value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
    Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
    Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

Examples:

    A few examples of transforming an arbitrary timestamp value to a RFC3339 timestamp string.

    >>> import utcnow
    >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00")
    "2023-09-07T02:18:00.000000Z"
    >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00", "+7d")
    "2023-09-14T02:18:00.000000Z"
    >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00+02:00")
    "2023-09-07T00:18:00.000000Z"
    >>> utcnow.rfc3339_timestamp(1693005993.285967)
    "2023-08-25T23:26:33.285967Z"
    >>> utcnow.rfc3339_timestamp()
    "2023-09-07T01:04:38.091041Z"  # current time

Returned timestamps follow RFC 3339 (Date and Time on the Internet: Timestamps): https://tools.ietf.org/html/rfc3339.

Timestamps are converted to UTC timezone which we'll note in the timestamp with the "Z" syntax instead of the also
accepted "+00:00". "Z" stands for UTC+0 or "Zulu time" and refers to the zone description of zero hours.

Timestamps are expressed as a date-time (not a Python datetime object), including the full date (the "T" between the
date and the time is optional in RFC 3339 (but not in ISO 8601) and usually describes the beginning of the time part.

Timestamps are 27 characters long in the format: "YYYY-MM-DDTHH:mm:ss.ffffffZ". 4 digit year, 2 digit month, 2 digit
days, "T", 2 digit hours, 2 digit minutes, 2 digit seconds, 6 fractional second digits (microseconds -> nanoseconds),
followed by the timezone identifier for UTC: "Z".

The library is specified to return timestamps with 6 fractional second digits, which means timestamps down to the
microsecond level. Having a six-digit fraction of a second is currently the most common way that timestamps are shown
at this date.
"""

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
from .protobuf import TimestampProtobufMessage

str_ = str

__author__: str_ = "Carl Oscar Aaro"
__email__: str_ = "hello@carloscar.com"

_SENTINEL = object()

# the following formats are accepted as date and date+time as string formatted input values.
# the library also accepts numeric values (int / float), specified as unixtime, or datetime objects.
# if no timezone is specified in input, utc is assumed.
_ACCEPTED_INPUT_FORMAT_VALUES = (
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S.%f %z",
    "%Y-%m-%d %H:%M:%S.%f %z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S %z",
    "%Y-%m-%d %H:%M:%S %z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M%z",
    "%Y-%m-%d %H:%M%z",
    "%Y-%m-%dT%H:%M %z",
    "%Y-%m-%d %H:%M %z",
    "%Y-%m-%d%z",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %z",
    "%Y-%m-%d",
)

# examples: "123", "-123", "123.456", "-123.456", "123.", "-123.", ".456", "-.456"
NUMERIC_REGEX = re.compile(r"^[-]?([0-9]+|[.][0-9]+|[0-9]+[.]|[0-9]+[.][0-9]+)$")

# examples: "2023-09-06T23:53:59.684762Z", "2023-09-06 23:53:59.684762+00:00"
PREFERRED_FORMAT_REGEX = re.compile(
    r"^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt ]([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9].[0-9]{6}([Zz]|[+-]00:00|)$"
)

# modifier multipliers: "s" (seconds), "m" (minutes), "h" (hours), "d" (days)
# example: a modifier value of "+10d" => add 10 days.
# example: a modifier value of "-1h" => subtract 1 hour.
MODIFIER_MUL = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
}

# datetime.timezone.utc
utc = UTC = timezone_.utc


@functools.lru_cache(maxsize=128, typed=False)
def _is_numeric(value: str_) -> bool:
    """
    Determines if a string represents a numeric value. A numeric values can optionally start with "-" (negative),
    optionally have a leading "." (decimal point) before any digit or can optionally end with "." (decimal point),
    meaning there is no decimal fragment present in the number.

    Args:
        value: A string to check for numeric representation.

    Returns:
        True if the string represents a numeric value, False otherwise.
    """
    if NUMERIC_REGEX.match(value):
        return True

    return False


def _init_modifier(
    value: Union[str_, datetime_, object, int, float, Decimal, Real, bytes, TimestampProtobufMessage],
    modifier: Optional[Union[str_, int, float]] = 0,
) -> Tuple[Union[str_, datetime_, object, int, float, Decimal, Real], Union[int, float]]:
    """
    Normalizes the input value + modifier tuple.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.
        modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
            Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
            Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

    Returns:
        A tuple containing the normalized value and the modifier.
    """
    if isinstance(value, TimestampProtobufMessage):
        value = value.seconds + round(value.nanos * 1e-9, 9)
    return _init_modifier_lru(value, modifier)


@functools.lru_cache(maxsize=128, typed=True)
def _init_modifier_lru(
    value: Union[str_, datetime_, object, int, bytes, float, Decimal, Real],
    modifier: Optional[Union[str_, int, float]] = 0,
) -> Tuple[Union[str_, datetime_, object, int, float, Decimal, Real], Union[int, float]]:
    """
    Normalizes the input value + modifier tuple.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.
        modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
            Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
            Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

    Returns:
        A tuple containing the normalized value and the modifier.
    """
    if isinstance(value, bytes):
        value_ = TimestampProtobufMessage()
        value_.MergeFromString(value)
        value = value_.seconds + round(value_.nanos * 1e-9, 9)

    if (
        value is not _SENTINEL
        and value
        and str_(value)[0] in ("+", "-")
        and not modifier
        and isinstance(value, str_)
        and value[-1] in MODIFIER_MUL
    ):
        modifier = value
        value = _SENTINEL

    if modifier is None:
        modifier = 0

    if isinstance(modifier, str_):
        modifier_mul: int = 1
        modifier_mul_str = modifier[-1]

        if len(modifier) > 1 and modifier_mul_str in MODIFIER_MUL and (modifier[-2].isdigit() or modifier[-2] == "."):
            modifier = modifier[:-1]
            modifier_mul = MODIFIER_MUL[modifier_mul_str]

        if "." in modifier:
            modifier = float(modifier) * modifier_mul
        else:
            modifier = int(modifier) * modifier_mul

    if value == "now":
        value = _SENTINEL

    return value, modifier


@functools.lru_cache(maxsize=128, typed=True)
def _transform_value(value: Union[str_, datetime_, object, int, float, Decimal, Real]) -> str_:
    """Transforms the input value to a timestamp string in RFC3339 format.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.

    Returns:
        The transformed value as a string in RFC3339 format.
    """
    str_value: str_
    try:
        if isinstance(value, str_):
            str_value = value.strip()
        elif isinstance(value, (int, float)):
            return datetime_.fromtimestamp(value, tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")
        elif isinstance(value, (Decimal, Real)):
            str_value = (
                datetime_.fromtimestamp(float(value), tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")
            )
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
            str_value = (
                datetime_.fromtimestamp(float(str_value), tz=UTC)
                .isoformat(timespec="microseconds")
                .replace("+00:00", "Z")
            )
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
    """Transforms the input value to a datetime object.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.

    Returns:
        The transformed value as a datetime object.
    """
    value = _transform_value(value)
    return datetime_.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")


@functools.lru_cache(maxsize=128)
def _timestamp_to_unixtime(value: str_) -> float:
    """Transforms the input value to a float value representing a timestamp as unixtime.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.

    Returns:
        The transformed value in unixtime (float).
    """
    return _timestamp_to_datetime(value).timestamp()


@functools.lru_cache(maxsize=128)
def _unixtime_to_protobuf(unixtime_value: Union[int, float]) -> TimestampProtobufMessage:
    """Transforms the unix timestamp input value to a google.protobuf.Timestamp protobuf message.

    Args:
        unixtime_value: A timestamp in unixtime format (float).

    Returns:
        The transformed value as a google.protobuf.Timestamp message.
    """
    seconds = int(unixtime_value)
    nanos = round(int((unixtime_value - seconds) * 1e6)) * 1000
    if nanos < 0:
        seconds -= 1
        nanos += 1_000_000_000
    return TimestampProtobufMessage(
        seconds=seconds,
        nanos=nanos,
    )


@functools.lru_cache(maxsize=128)
def _timezone_from_string(value: str_) -> Optional[tzinfo_]:
    """Converts a string to a timezone object.

    Args:
        value: A string representing a 0-offset timezone (UTC) or a timezone string as an offset (for example: +HH:mm).

    Returns:
        A timezone object if the string represents a valid timezone, otherwise None.
    """
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

    def __call__(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        modifier: Optional[Union[str_, int, float]] = 0,
    ) -> str_:
        """Transforms the input value to a timestamp string in RFC3339 format.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The transformed value as a string in RFC3339 format.

        Raises:
            ValueError: If the input value does not match allowed input formats.
        """
        value, modifier = _init_modifier(value, modifier)

        if value is _SENTINEL:
            return (
                (datetime_.now(UTC) if not modifier else datetime_.now(UTC) + timedelta_(seconds=modifier))
                .isoformat(timespec="microseconds")
                .replace("+00:00", "Z")
            )
        return _transform_value(value) if not modifier else _transform_value(_timestamp_to_unixtime(value) + modifier)


class now_(_baseclass):
    def __new__(cls, *args: Any) -> now_:
        result = object.__new__(cls, *args)

        return result

    def __str__(self) -> str_:
        return datetime_.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")

    def __repr__(self) -> str_:
        return datetime_.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


class utcnow_(_baseclass):
    now = now_()

    def __new__(cls, *args: Any) -> utcnow_:
        result = object.__new__(cls, *args)

        return result

    def as_string(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        modifier: Optional[Union[str_, int, float]] = 0,
    ) -> str_:
        """Transforms the input value to a timestamp string in RFC3339 format.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The transformed value as a string in RFC3339 format.

        Raises:
            ValueError: If the input value does not match allowed input formats.

        Examples:
            >>> import utcnow
            >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00")
            "2023-09-07T02:18:00.000000Z"
            >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00", "+7d")
            "2023-09-14T02:18:00.000000Z"
            >>> utcnow.rfc3339_timestamp("2023-09-07 02:18:00+02:00")
            "2023-09-07T00:18:00.000000Z"
            >>> utcnow.rfc3339_timestamp(1693005993.285967)
            "2023-08-25T23:26:33.285967Z"
            >>> from datetime import datetime, timezone, timedelta
            >>> tz = timezone(timedelta(hours=2, minutes=0))
            >>> dt = datetime(2023, 4, 30, 8, 0, 0, tzinfo=tz)
            >>> utcnow.rfc3339_timestamp(dt)
            "2023-04-30T06:00:00.000000Z"
        """
        value, modifier = _init_modifier(value, modifier)

        if value is _SENTINEL:
            return (
                (datetime_.now(UTC) if not modifier else datetime_.now(UTC) + timedelta_(seconds=modifier))
                .isoformat(timespec="microseconds")
                .replace("+00:00", "Z")
            )
        return _transform_value(value) if not modifier else _transform_value(_timestamp_to_unixtime(value) + modifier)

    def as_datetime(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        modifier: Optional[Union[str_, int, float]] = 0,
    ) -> datetime_:
        """Transforms the input value to a datetime object.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The transformed value as a datetime object.

        Raises:
            ValueError: If the input value does not match allowed input formats.

        Examples:
            >>> import utcnow
            >>> utcnow.as_datetime("2023-08-01 12:10:59.123456+02:00")
            datetime.datetime(2023, 8, 1, 10, 10, 59, 123456, tzinfo=datetime.timezone.utc)
        """
        value, modifier = _init_modifier(value, modifier)

        if value is _SENTINEL:
            # 'datetime.datetime.now(UTC)' is faster than (deprecated) 'datetime.datetime.utcnow().replace(tzinfo=UTC)'
            return datetime_.now(UTC) if not modifier else datetime_.now(UTC) + timedelta_(seconds=modifier)
        return _timestamp_to_datetime(value) if not modifier else datetime_.now(UTC) + timedelta_(seconds=modifier)

    def as_unixtime(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        modifier: Optional[Union[str_, int, float]] = 0,
    ) -> float:
        """Transforms the input value to a float value representing a timestamp as unixtime.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The transformed value in unixtime (float).

        Raises:
            ValueError: If the input value does not match allowed input formats.

        Examples:
            >>> import utcnow
            >>> utcnow.as_unixtime("1970-01-01T00:00:00.000000Z")
            0.0
            >>> utcnow.as_unixtime("1970-01-01T00:00:00.000000Z", "+24h")
            86400.0
            >>> utcnow.as_unixtime("2022-01-01 00:00:00.123456+00:00")
            1640995200.123456
        """
        value, modifier = _init_modifier(value, modifier)

        if value is _SENTINEL:
            return time_.time() + modifier
        return _timestamp_to_unixtime(value) + modifier

    def as_protobuf(
        self,
        value: Union[str_, datetime_, object, int, float, Decimal, Real] = _SENTINEL,
        modifier: Optional[Union[str_, int, float]] = 0,
    ) -> TimestampProtobufMessage:
        """Transforms the input value to a google.protobuf.Timestamp protobuf message.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The transformed value as a google.protobuf.Timestamp message.

        Raises:
            ValueError: If the input value does not match allowed input formats.

        Examples:
            >>> import utcnow
            >>> utcnow.as_protobuf("2022-01-01 00:00:00.123456+00:00")
            seconds: 1640995200
            nanos: 123456000
            >>> utcnow.as_protobuf(1234567890.05, modifier=-0.1)
            seconds: 1234567889
            nanos: 950000000
        """
        value, modifier = _init_modifier(value, modifier)

        if value is _SENTINEL:
            unixtime_value = time_.time() + modifier
            seconds = int(unixtime_value)
            nanos = round(int((unixtime_value - seconds) * 1e6)) * 1000
            if nanos < 0:
                seconds -= 1
                nanos += 1_000_000_000
            return TimestampProtobufMessage(
                seconds=seconds,
                nanos=nanos,
            )

        return _unixtime_to_protobuf(_timestamp_to_unixtime(value) + modifier)

    def timediff(
        self,
        begin: Union[str_, datetime_, object, int, float, Decimal, Real],
        end: Union[str_, datetime_, object, int, float, Decimal, Real],
        unit: str_ = "seconds",
    ) -> float:
        """Calculate the time difference between two timestamps.

        Args:
            begin: The beginning timestamp. Can be a string, datetime object, or a numeric unixtime value.
            end: The ending timestamp. Can be a string, datetime object, or a numeric unixtime value.
            unit: The unit of time to return the difference in. Defaults to "seconds".

        Returns:
            The time difference between the two timestamps in the specified unit.

        Raises:
            ValueError: If an unknown unit is specified.

        Examples:
            >>> from utcnow import timediff
            >>> timediff("2022-01-01 00:00:00", "2022-01-01 00:00:10")
            10.0
            >>> timediff("2022-01-01 00:00:00", "2022-01-01 00:01:00", unit="minutes")
            1.0
            >>> timediff("2022-01-01 00:00:00", "2022-01-02 00:00:00", unit="days")
            1.0
            >>> timediff("2022-01-01T00:00:00.000000Z", "2022-01-02T06:00:00.000000Z", unit="days")
            1.25
            >>> timediff(0, 7200, unit="hours")
            2.0
        """
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
        """Transforms the input value to a string representing a date (YYYY-mm-dd) without timespec or timezone.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            tz: An optional timezone for which the date is represented related to the input value.
                If not specified, UTC timezone will be applied.

        Returns:
            A string representing a date (YYYY-mm-dd) without timespec or timezone.

        Raises:
            ValueError: If the input value does not match allowed input formats.

        Examples:
            >>> import utcnow
            >>> utcnow.as_date_string("2023-09-07 02:18:00")
            "2023-09-07"
            >>> utcnow.as_date_string("2020-01-01T00:00:00.000000Z")
            "2020-01-01"
            >>> utcnow.as_date_string("2020-01-01T00:00:00.000000+02:00")
            "2019-12-31"
            >>> utcnow.as_date_string("2020-01-01T00:00:00.000000+02:00", "+02:00")
            "2020-01-01"
            >>> utcnow.as_date_string(1234567890.123456)
            "2009-02-13"
            >>> utcnow.as_date_string(0)
            "1970-01-01"
            >>> utcnow.as_date_string()
            "2023-09-07"  # current date
        """
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

        if value is _SENTINEL or value == "now":
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

    as_proto = as_protobuf
    as_protobuf_timestamp = as_protobuf
    as_proto_timestamp = as_protobuf
    as_pb = as_protobuf
    to_protobuf = as_protobuf
    to_proto = as_protobuf
    to_protobuf_timestamp = as_protobuf
    to_proto_timestamp = as_protobuf
    to_pb = as_protobuf
    get_protobuf = as_protobuf
    get_proto = as_protobuf
    get_protobuf_timestamp = as_protobuf
    get_proto_timestamp = as_protobuf
    get_pb = as_protobuf
    protobuf = as_protobuf
    proto = as_protobuf
    protobuf_timestamp = as_protobuf
    proto_timestamp = as_protobuf
    pb = as_protobuf

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

as_protobuf = _module_value.as_protobuf
as_proto = as_protobuf
as_protobuf_timestamp = as_protobuf
as_proto_timestamp = as_protobuf
as_pb = as_protobuf
to_protobuf = as_protobuf
to_proto = as_protobuf
to_protobuf_timestamp = as_protobuf
to_proto_timestamp = as_protobuf
to_pb = as_protobuf
get_protobuf = as_protobuf
get_proto = as_protobuf
get_protobuf_timestamp = as_protobuf
get_proto_timestamp = as_protobuf
get_pb = as_protobuf
protobuf = as_protobuf
proto = as_protobuf
protobuf_timestamp = as_protobuf
proto_timestamp = as_protobuf
pb = as_protobuf

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
