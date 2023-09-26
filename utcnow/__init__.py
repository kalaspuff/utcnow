"""Package for formatting arbitrary timestamps as strict RFC 3339.

Timestamps as RFC 3339 (Date & Time on the Internet) formatted strings with conversion functionality from other
timestamp formats or for timestamps on other timezones. Additionally converts timestamps from datetime objects
and other common date utilities.

``utcnow.rfc3339_timestamp(value, modifier)``
    Transforms the input value to a timestamp string in RFC 3339 format.
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
    A few examples of transforming an arbitrary timestamp value to a RFC 3339 timestamp string.

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

See also:
``utcnow.as_date_string(value, tz)``
    Transforms the input value to a string representing a date (YYYY-mm-dd) without timespec or indicated timezone.
    An optional ``tz`` argument can be used to return the date in the specific timezone.
``utcnow.today(tz)``
    Returns a string representing today's date (YYYY-mm-dd) without timespec or indicated timezone.
    An optional ``tz`` argument can be used to return today's date in the specific timezone.
``utcnow.timediff(begin, end, unit)``
    Calculate the time difference between two timestamps.
``utcnow.synchronizer``
    Freeze the current time in ``utcnow`` with the ``utcnow.synchronizer`` context manager.
"""

from __future__ import annotations

import sys

if __name__ not in sys.modules or not getattr(sys.modules[__name__], "__original_module__", None):
    import datetime as datetime_
    import functools
    import re
    import sys
    import time as time_
    import warnings
    from datetime import datetime, timedelta, timezone, tzinfo
    from decimal import Decimal
    from numbers import Real
    from types import FunctionType, ModuleType
    from typing import Any, Callable, Dict, Generic, Optional, Tuple, Type, TypeVar, Union, cast

    from .__version_data__ import __version__, __version_info__
    from .protobuf import TimestampProtobufMessage

    __author__: str = "Carl Oscar Aaro"
    __email__: str = "hello@carloscar.com"

    # sentinel
    NOW = TODAY = object()

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

    # common modifier multipliers: "s" (seconds), "m" (minutes), "h" (hours), "d" (days)
    # precision modifier multiplicers: "ns" (nanoseconds), "us" (microseconds), "ms" (milliseconds)
    # example: a modifier value of "+10d" => add 10 days.
    # example: a modifier value of "-1h" => subtract 1 hour.
    MODIFIER_MUL = {
        "ns": 1e-9,
        "us": 1e-6,
        "µs": 1e-6,
        "ms": 1e-3,
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }

    # datetime.timezone.utc
    utc = UTC = timezone.utc

    # time synchronizer context manager
    TS = TypeVar("TS", bound="TimeSynchronizer")

    class TimeSynchronizer(Generic[TS]):
        """Creates a context manager that when used sets the current time in calls to the utcnow library to return
            the deterministic value of the context manager.

        Args:
            value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
            modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000
                seconds). Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

        Returns:
            The utcnow.synchronizer object initialized on the specified time and eventual modifier.

        Raises:
            ValueError: If the input value does not match allowed input formats.
            RuntimeError: If an utcnow.synchronizer context has already been opened or if the same synchronizer
                context is invalidly used, either multiple times or if the context has expired (replaced by a
                more recently initiated synchronizer context).

        Examples:
            >>> import utcnow
            >>> with utcnow.synchronizer:
                    created_time = utcnow.rfc3339_timestamp()
                    expire_time = utcnow.rfc3339_timestamp("now", "+15m")
            >>> utcnow.timediff(created_time, expire_time, "seconds")
            900.0
        """

        _frozen: bool
        _synchronizer: TimeSynchronizer[TS]
        _controller: Optional[TimeSynchronizer[TS]]
        _datetime: datetime_.datetime
        _time_ns: int

        def __new__(cls: Type[TS]) -> TimeSynchronizer[TS]:
            result = super().__new__(cls)
            result._frozen = False

            if not getattr(cls, "_synchronizer", None):
                cls._synchronizer = result
                result._controller = None

            return result

        def __call__(
            self,
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
        ) -> TimeSynchronizer[TS]:
            """Creates a context manager that when used sets the current time in calls to the utcnow library to return
                the deterministic value of the context manager.

            Args:
                value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
                modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                    Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000
                    seconds). Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

            Returns:
                The utcnow.synchronizer object initialized on the specified time and eventual modifier.

            Raises:
                ValueError: If the input value does not match allowed input formats.
                RuntimeError: If an utcnow.synchronizer context has already been opened or if the same synchronizer
                    context is invalidly used, either multiple times or if the context has expired (replaced by a
                    more recently initiated synchronizer context).

            Examples:
                >>> import utcnow
                >>> with utcnow.synchronizer:
                        created_time = utcnow.rfc3339_timestamp()
                        expire_time = utcnow.rfc3339_timestamp("now", "+15m")
                >>> utcnow.timediff(created_time, expire_time, "seconds")
                900.0
            """
            if self._synchronizer._frozen is True:
                raise RuntimeError("'utcnow.synchronizer' context cannot be nested (library time already synchronized)")
            if self._synchronizer is not self:
                raise RuntimeError("use the main 'utcnow.synchronizer' to initialize a new context manager")

            cls = type(self)
            self._synchronizer._controller = None
            self_ = cls()

            if value is NOW and modifier == 0:
                self_._time_ns = int(round(time_.time_ns() * 1e-3)) * 1_000
                self_._datetime = datetime_.datetime.fromtimestamp(round(self_._time_ns * 1e-9, 6), tz=UTC)
            else:
                value, modifier = _init_modifier(value, modifier)
                if value is not NOW:
                    self_._datetime = (
                        _timestamp_to_datetime(value)
                        if not modifier
                        else _timestamp_to_datetime(value) + timedelta(seconds=modifier)
                    )
                    self_._time_ns = int(round(self_._datetime.timestamp() * 1e6)) * 1_000
                else:
                    self_._time_ns = int(round(time_.time_ns() * 1e-3)) * 1_000 + int(round(modifier * 1e6)) * 1_000
                    self_._datetime = datetime_.datetime.fromtimestamp(round(self_._time_ns * 1e-9, 6), tz=UTC)

            self._synchronizer._controller = self_
            return self_

        def __enter__(
            self,
        ) -> TimeSynchronizer[TS]:
            """Opens a context manager that sets the current time in calls to the utcnow library to return
                the current time as a deterministic value either set as part of 'utcnow.synchronizer()' initation as or
                fallback using the current time of when the context manager was opened.

            Returns:
                The utcnow.synchronizer value.

            Raises:
                RuntimeError: If an utcnow.synchronizer context has already been opened or if the same synchronizer
                    context is invalidly used either multiple times or has expired and been replaced by another
                    synchronizer.

            Examples:
                >>> import utcnow
                >>> with utcnow.synchronizer:
                        created_time = utcnow.rfc3339_timestamp()
                        expire_time = utcnow.rfc3339_timestamp("now", "+15m")
                >>> utcnow.timediff(created_time, expire_time, "seconds")
                900.0
            """
            if self._frozen is True or self._synchronizer._frozen is True:
                raise RuntimeError("'utcnow.synchronizer' context cannot be nested (library time already synchronized)")

            if self._synchronizer is not self:
                if self._synchronizer._controller is not self:
                    raise RuntimeError(
                        "'utcnow.synchronizer' context must be initiated from the newly created child synchronizer"
                    )

                self._frozen = True
                self._synchronizer._time_ns = self._time_ns
                self._synchronizer._datetime = self._datetime
                return self._synchronizer.__enter__()

            if self._synchronizer._controller is not None and self._synchronizer._controller._frozen is False:
                self._synchronizer._controller = None

            if self._synchronizer._controller is None:
                self._time_ns = int(round(time_.time_ns() * 1e-3)) * 1_000
                self._datetime = datetime_.datetime.fromtimestamp(round(self._time_ns * 1e-9, 6), tz=UTC)

            self._frozen = True
            return self

        def __exit__(self, *args: Any, **kwargs: Any) -> None:
            if (
                self._synchronizer is not self
                and self._synchronizer._controller is self
                and self._synchronizer._frozen is True
            ):
                self._synchronizer.__exit__(*args, **kwargs)
            elif self._synchronizer is self and self._frozen is True:
                self._frozen = False
                self._controller = None

        def __repr__(self) -> str:
            if self._synchronizer is not self:
                value = self._datetime.isoformat(timespec="microseconds").replace("+00:00", "Z")
                if self._synchronizer._controller is not self:
                    if self._frozen:
                        return (
                            f"<utcnow.synchronizer [child: {hex(id(self))}] (deactivated context) timestamp='{value}'>"
                        )
                    return f"<utcnow.synchronizer [child: {hex(id(self))}] (expired) timestamp='{value}'>"
                if self._frozen is True and self._synchronizer._frozen is True:
                    return f"<utcnow.synchronizer [child: {hex(id(self))}] (active context) timestamp='{value}'>"
                return f"<utcnow.synchronizer [child: {hex(id(self))}] (pending context) timestamp='{value}'>"

            if self._frozen:
                value = self._datetime.isoformat(timespec="microseconds").replace("+00:00", "Z")
                return f"<utcnow.synchronizer [main: {hex(id(self))}] (active context) timestamp='{value}'>"

            return f"<utcnow.synchronizer [main: {hex(id(self))}]>"

        def __eq__(self, other: Any) -> bool:
            return bool(other is self)

        @property
        def frozen(self) -> bool:
            return self._frozen

        @property
        def datetime(self) -> datetime_.datetime:
            return self._datetime if self._frozen is True else datetime_.datetime.now(UTC)

        @property
        def time(self) -> float:
            return round(self._time_ns * 1e-9 if self._frozen is True else self.time_ns * 1e-9, 6)

        @property
        def time_ns(self) -> float:
            return self._time_ns if self._frozen is True else int(round(time_.time_ns() * 1e-3)) * 1_000

    __synchronizer: Type[TimeSynchronizer] = type(
        "synchronizer", (TimeSynchronizer,), {"__doc__": TimeSynchronizer.__doc__}
    )
    __synchronizer__ = synchronizer = TimeSynchronizer.__new__(__synchronizer)

    CT = TypeVar("CT", bound=Callable)

    @functools.lru_cache(maxsize=128, typed=False)
    def _is_numeric(value: str) -> bool:
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
        value: Union[str, datetime, object, int, float, Decimal, Real, bytes, TimestampProtobufMessage],
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> Tuple[Union[str, datetime, object, int, float, Decimal, Real], Union[int, float]]:
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
        value: Union[str, datetime, object, int, bytes, float, Decimal, Real],
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> Tuple[Union[str, datetime, object, int, float, Decimal, Real], Union[int, float]]:
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
            value is not NOW
            and value
            and str(value)[0] in ("+", "-")
            and not modifier
            and isinstance(value, str)
            and (value[-1] in MODIFIER_MUL or value[-2:] in MODIFIER_MUL)
        ):
            modifier = value
            value = NOW

        if modifier is None:
            modifier = 0

        if isinstance(modifier, str):
            modifier_mul: int = 1
            modifier_mul_str = modifier[-1] if modifier[-2:] not in MODIFIER_MUL else modifier[-2:]

            if (
                len(modifier) > 1
                and modifier_mul_str in MODIFIER_MUL
                and len(modifier) > len(modifier_mul_str)
                and (modifier[-(len(modifier_mul_str) + 1)].isdigit() or modifier[-(len(modifier_mul_str) + 1)] == ".")
            ):
                modifier = modifier[: -len(modifier_mul_str)]
                modifier_mul = MODIFIER_MUL[modifier_mul_str]

            if "." in modifier:
                modifier = float(modifier) * modifier_mul
            else:
                modifier = int(modifier) * modifier_mul

        if isinstance(value, str) and str(value).lower() in ("now", "today"):
            value = NOW

        return value, modifier

    @functools.lru_cache(maxsize=128, typed=True)
    def _transform_value(value: Union[str, datetime, object, int, float, Decimal, Real]) -> str:
        """Transforms the input value to a timestamp string in RFC 3339 format.

        Args:
            value: A value representing a timestamp in any of the allowed input formats.

        Returns:
            The transformed value as a string in RFC 3339 format.
        """
        str_value: str
        try:
            if isinstance(value, str):
                str_value = value.strip()
            elif isinstance(value, (int, float)):
                return datetime.fromtimestamp(value, tz=UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")
            elif isinstance(value, (Decimal, Real)):
                str_value = (
                    datetime.fromtimestamp(float(value), tz=UTC)
                    .isoformat(timespec="microseconds")
                    .replace("+00:00", "Z")
                )
            else:
                str_value = str(value).strip()

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
                    datetime.fromtimestamp(float(str_value), tz=UTC)
                    .isoformat(timespec="microseconds")
                    .replace("+00:00", "Z")
                )
        except Exception:
            raise ValueError(
                f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats"
            )

        if PREFERRED_FORMAT_REGEX.match(str_value):
            if int(str_value[8:10]) >= 30 or (int(str_value[5:7]) == 2 and int(str_value[8:10]) >= 28):
                try:
                    dt_value = datetime.strptime(str_value[0:10], "%Y-%m-%d")
                except ValueError:
                    raise ValueError(
                        f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats"
                    )
            return (str_value[:10] + "T" + str_value[11:]).upper().rstrip("Z").rsplit("+00:00")[0].rsplit("-00:00")[
                0
            ] + "Z"

        ends_with_utc = False
        if str_value.endswith(" UTC"):
            str_value = str_value[0:-4]
            ends_with_utc = True

        for format_ in _ACCEPTED_INPUT_FORMAT_VALUES:
            try:
                dt_value = datetime.strptime(str_value, format_)
            except ValueError:
                continue

            if ends_with_utc and dt_value.tzinfo:
                raise ValueError(
                    f"The input value '{value}' (type: {value.__class__}) uses double timezone declaration: 'UTC' and '{dt_value.tzinfo}'"
                )

            break
        else:
            raise ValueError(
                f"The input value '{value}' (type: {value.__class__}) does not match allowed input formats"
            )

        if not dt_value.tzinfo:
            # Timezone declaration missing, skipping tz application and blindly assuming UTC
            return dt_value.isoformat(timespec="microseconds") + "Z"

        return dt_value.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")

    @functools.lru_cache(maxsize=128)
    def _timestamp_to_datetime(value: str) -> datetime:
        """Transforms the input value to a datetime object.

        Args:
            value: A value representing a timestamp in any of the allowed input formats.

        Returns:
            The transformed value as a datetime object.
        """
        value = _transform_value(value)
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")

    @functools.lru_cache(maxsize=128)
    def _timestamp_to_unixtime(value: str) -> float:
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
        nanos = int(round((unixtime_value - seconds) * 1e6)) * 1_000
        if nanos < 0:
            seconds -= 1
            nanos += 1_000_000_000
        return TimestampProtobufMessage(
            seconds=seconds,
            nanos=nanos,
        )

    @functools.lru_cache(maxsize=128)
    def _timezone_from_string(value: str) -> Optional[tzinfo]:
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

            td = timedelta(hours=int(m.group(1)), minutes=int(m.group(2)))
            if td.days == 1 and td == timedelta(days=1):
                td = timedelta(days=1, microseconds=-1)

            return timezone(modifier * td)

        return None

    class _metaclass(type):
        def __new__(cls: Type[_metaclass], name: str, bases: Tuple[type, ...], attributedict: Dict) -> _metaclass:
            result = cast(Type["_baseclass"], super().__new__(cls, name, bases, dict(attributedict)))

            return result

    class _baseclass(metaclass=_metaclass):
        def __init__(self) -> None:
            pass

        def __call__(
            self,
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
        ) -> str:
            """Transforms the input value to a timestamp string in RFC 3339 format.

            Args:
                value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
                modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                    Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                    Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

            Returns:
                The transformed value as a string in RFC 3339 format.

            Raises:
                ValueError: If the input value does not match allowed input formats.
            """
            value, modifier = _init_modifier(value, modifier)

            if value is NOW:
                return (
                    (synchronizer.datetime if not modifier else synchronizer.datetime + timedelta(seconds=modifier))
                    .isoformat(timespec="microseconds")
                    .replace("+00:00", "Z")
                )
            return (
                _transform_value(value) if not modifier else _transform_value(_timestamp_to_unixtime(value) + modifier)
            )

    def _deprecation_decorator(func: CT, deprecated_func_name: str) -> CT:
        @functools.wraps(func)
        def _wrapper(*a: Any, **kw: Any) -> Any:
            warnings.warn(
                f"Using the '{deprecated_func_name}()' function alias is deprecated. Use the 'utcnow.{getattr(func, '__name__') if getattr(func, '__name__', None) else func.__func__.__name__}()' function instead.",
                DeprecationWarning,
            )

            if isinstance(func, staticmethod):
                return func.__func__(*a, **kw)
            return func(*a, **kw)

        return cast(CT, staticmethod(_wrapper))

    NT = TypeVar("NT", bound="now_")
    UT = TypeVar("UT", bound="utcnow_")

    class now_(_baseclass):
        def __new__(cls: Type[NT], *args: Any) -> NT:
            result = object.__new__(cls, *args)
            return result

        def __str__(self) -> str:
            return synchronizer.datetime.isoformat(timespec="microseconds").replace("+00:00", "Z")

        def __repr__(self) -> str:
            return synchronizer.datetime.isoformat(timespec="microseconds").replace("+00:00", "Z")

    class utcnow_(_baseclass):
        now = type("now", (now_,), {})()

        def __new__(cls: Type[UT], *args: Any) -> UT:
            result = object.__new__(cls, *args)

            for attr in dir(cls):
                if any(
                    (
                        attr.startswith("_"),
                        not callable(getattr(result, attr)),
                        not isinstance(getattr(result, attr), FunctionType),
                        "." not in getattr(getattr(result, attr), "__qualname__", "."),
                    )
                ):
                    continue

                func = getattr(result, attr)
                func.__qualname__ = getattr(getattr(result, attr), "__qualname__", ".").rsplit(".", 1)[-1]

            return result

        @staticmethod
        def rfc3339_timestamp(
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
        ) -> str:
            """Transforms the input value to a timestamp string in RFC 3339 format.

            Args:
                value: A value representing a timestamp in any of the allowed input formats, or "now" if left unset.
                modifier: An optional modifier to be added to the Unix timestamp of the value. Defaults to 0.
                    Can be specified in seconds (int or float) or as string, for example "+10d" (10 days => 864000 seconds).
                    Can also be set to a negative value, for example "-1h" (1 hour => -3600 seconds).

            Returns:
                The transformed value as a string in RFC 3339 format.

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

            if value is NOW:
                return (
                    (synchronizer.datetime if not modifier else synchronizer.datetime + timedelta(seconds=modifier))
                    .isoformat(timespec="microseconds")
                    .replace("+00:00", "Z")
                )
            return (
                _transform_value(value) if not modifier else _transform_value(_timestamp_to_unixtime(value) + modifier)
            )

        @staticmethod
        def as_datetime(
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
        ) -> datetime:
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

            if value is NOW:
                return synchronizer.datetime if not modifier else synchronizer.datetime + timedelta(seconds=modifier)
            return (
                _timestamp_to_datetime(value)
                if not modifier
                else _timestamp_to_datetime(value) + timedelta(seconds=modifier)
            )

        @staticmethod
        def as_unixtime(
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
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

            if value is NOW:
                return synchronizer.time + modifier
            return _timestamp_to_unixtime(value) + modifier

        @staticmethod
        def as_protobuf(
            value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
            modifier: Optional[Union[str, int, float]] = 0,
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

            if value is NOW:
                unixtime_value = synchronizer.time + modifier
                seconds = int(unixtime_value)
                nanos = int(round((unixtime_value - seconds) * 1e6)) * 1_000
                if nanos < 0:
                    seconds -= 1
                    nanos += 1_000_000_000
                return TimestampProtobufMessage(
                    seconds=seconds,
                    nanos=nanos,
                )

            return _unixtime_to_protobuf(_timestamp_to_unixtime(value) + modifier)

        @staticmethod
        def timediff(
            begin: Union[str, datetime, object, int, float, Decimal, Real],
            end: Union[str, datetime, object, int, float, Decimal, Real],
            unit: str = "seconds",
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
                >>> import utcnow
                >>> utcnow.timediff("2022-01-01 00:00:00", "2022-01-01 00:00:10")
                10.0
                >>> utcnow.timediff("2022-01-01 00:00:00", "2022-01-01 00:01:00", unit="minutes")
                1.0
                >>> utcnow.timediff("2022-01-01 00:00:00", "2022-01-02 00:00:00", unit="days")
                1.0
                >>> utcnow.timediff("2022-01-01T00:00:00.000000Z", "2022-01-02T06:00:00.000000Z", unit="days")
                1.25
                >>> utcnow.timediff(0, 7200, unit="hours")
                2.0
            """
            if synchronizer.frozen is False:
                with synchronizer:
                    delta = utcnow_.as_datetime(end) - utcnow_.as_datetime(begin)
            else:
                delta = utcnow_.as_datetime(end) - utcnow_.as_datetime(begin)

            unit = unit.lower()

            if unit in ("nanoseconds", "nanosecond", "nsec", "ns", "nanos", "nano", "nanosec"):
                return int(delta.total_seconds() * 1e6) * 1_000
            if unit in ("microseconds", "microsecond", "usec", "us", "micros", "micro", "microsec", "µs"):
                return delta.total_seconds() * 1e6
            if unit in ("milliseconds", "millisecond", "msec", "ms", "millis", "milli", "millisec"):
                return delta.total_seconds() * 1e3
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

        @staticmethod
        def as_date_string(
            value: Union[str, datetime, object, int, float, Decimal, Real] = TODAY,
            tz: Optional[Union[str, tzinfo]] = None,
        ) -> str:
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
            date_tz: Optional[tzinfo] = None

            if not tz:
                date_tz = UTC
            elif isinstance(tz, tzinfo):
                date_tz = tz
            elif isinstance(tz, str):
                date_tz = _timezone_from_string(tz)

            if not date_tz:
                raise ValueError(
                    f"Unknown timezone value '{tz}' (type: {tz.__class__.__name__}) - use value of type 'datetime.tzinfo' or an utcoffset string value"
                )

            if value is TODAY or (isinstance(value, str) and str(value).lower() in ("now", "today")):
                return datetime_.datetime.fromtimestamp(synchronizer.time, tz=date_tz).date().isoformat()

            return _timestamp_to_datetime(value).astimezone(date_tz).date().isoformat()

        @staticmethod
        def today(
            tz: Optional[Union[str, tzinfo]] = None,
        ) -> str:
            """Returns a string representing today's date (YYYY-mm-dd) without timespec or timezone.

            Args:
                tz: An optional timezone value that is used to return today's date in the specific timezone.
                    If not specified, UTC timezone will be applied. Note that the timezone value will not be
                    represented in the returned value, only the current date (YYYY-mm-dd) in the specified timezone.

            Returns:
                A string representing today's date (YYYY-mm-dd) without timespec or timezone.

            Raises:
                ValueError: If the input value does not match allowed input formats.

            Examples:
                >>> import pytz
                >>> import utcnow
                >>> utcnow.rfc3339_timestamp()
                "2023-09-07T23:31:25.134196Z"  # current time
                >>> utcnow.today()
                "2023-09-07"  # current date
                >>> timezone = pytz.timezone("Europe/Stockholm")  # UTC+02:00
                >>> utcnow.today(tz=timezone)
                "2023-09-08"  # current date in Europe/Stockholm timezone
                >>> utcnow.today(tz="+01:00")
                "2023-09-08"  # current date in a timezone with UTC offset +01:00
            """
            return utcnow_.as_date_string(tz=tz)

        synchronizer = synchronizer

        as_string = rfc3339_timestamp
        get = rfc3339_timestamp

        as_str = _deprecation_decorator(rfc3339_timestamp, "utcnow.as_str")
        as_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.as_rfc3339")
        to_string = _deprecation_decorator(rfc3339_timestamp, "utcnow.to_string")
        to_str = _deprecation_decorator(rfc3339_timestamp, "utcnow.to_str")
        to_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.to_rfc3339")
        get_string = _deprecation_decorator(rfc3339_timestamp, "utcnow.get_string")
        get_str = _deprecation_decorator(rfc3339_timestamp, "utcnow.get_str")
        get_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.get_rfc3339")
        string = _deprecation_decorator(rfc3339_timestamp, "utcnow.string")
        rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.rfc3339")
        timestamp_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.timestamp_rfc3339")
        ts_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.ts_rfc3339")
        rfc3339_ts = _deprecation_decorator(rfc3339_timestamp, "utcnow.rfc3339_ts")
        utcnow_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.utcnow_rfc3339")
        rfc3339_utcnow = _deprecation_decorator(rfc3339_timestamp, "utcnow.rfc3339_utcnow")
        now_rfc3339 = _deprecation_decorator(rfc3339_timestamp, "utcnow.now_rfc3339")
        rfc3339_now = _deprecation_decorator(rfc3339_timestamp, "utcnow.rfc3339_now")
        get_now = _deprecation_decorator(rfc3339_timestamp, "utcnow.get_now")

        as_date = _deprecation_decorator(as_datetime, "utcnow.as_date")
        as_dt = _deprecation_decorator(as_datetime, "utcnow.as_dt")
        to_datetime = _deprecation_decorator(as_datetime, "utcnow.to_datetime")
        to_date = _deprecation_decorator(as_datetime, "utcnow.to_date")
        to_dt = _deprecation_decorator(as_datetime, "utcnow.to_dt")
        get_datetime = _deprecation_decorator(as_datetime, "utcnow.get_datetime")
        get_date = _deprecation_decorator(as_datetime, "utcnow.get_date")
        get_dt = _deprecation_decorator(as_datetime, "utcnow.get_dt")
        date = _deprecation_decorator(as_datetime, "utcnow.date")
        dt = _deprecation_decorator(as_datetime, "utcnow.dt")

        as_unix = _deprecation_decorator(as_unixtime, "utcnow.as_unix")
        as_time = _deprecation_decorator(as_unixtime, "utcnow.as_time")
        as_timestamp = _deprecation_decorator(as_unixtime, "utcnow.as_timestamp")
        as_ut = _deprecation_decorator(as_unixtime, "utcnow.as_ut")
        as_ts = _deprecation_decorator(as_unixtime, "utcnow.as_ts")
        as_float = _deprecation_decorator(as_unixtime, "utcnow.as_float")
        to_unixtime = _deprecation_decorator(as_unixtime, "utcnow.to_unixtime")
        to_unix = _deprecation_decorator(as_unixtime, "utcnow.to_unix")
        to_time = _deprecation_decorator(as_unixtime, "utcnow.to_time")
        to_timestamp = _deprecation_decorator(as_unixtime, "utcnow.to_timestamp")
        to_ut = _deprecation_decorator(as_unixtime, "utcnow.to_ut")
        to_ts = _deprecation_decorator(as_unixtime, "utcnow.to_ts")
        to_float = _deprecation_decorator(as_unixtime, "utcnow.to_float")
        get_unixtime = _deprecation_decorator(as_unixtime, "utcnow.get_unixtime")
        get_unix = _deprecation_decorator(as_unixtime, "utcnow.get_unix")
        get_time = _deprecation_decorator(as_unixtime, "utcnow.get_time")
        get_timestamp = _deprecation_decorator(as_unixtime, "utcnow.get_timestamp")
        get_ut = _deprecation_decorator(as_unixtime, "utcnow.get_ut")
        get_ts = _deprecation_decorator(as_unixtime, "utcnow.get_ts")
        get_float = _deprecation_decorator(as_unixtime, "utcnow.get_float")
        unixtime = _deprecation_decorator(as_unixtime, "utcnow.unixtime")
        unix = _deprecation_decorator(as_unixtime, "utcnow.unix")
        time = _deprecation_decorator(as_unixtime, "utcnow.time")
        timestamp = _deprecation_decorator(as_unixtime, "utcnow.timestamp")
        ut = _deprecation_decorator(as_unixtime, "utcnow.ut")
        ts = _deprecation_decorator(as_unixtime, "utcnow.ts")

        as_proto = _deprecation_decorator(as_protobuf, "utcnow.as_proto")
        as_protobuf_timestamp = _deprecation_decorator(as_protobuf, "utcnow.as_protobuf_timestamp")
        as_proto_timestamp = _deprecation_decorator(as_protobuf, "utcnow.as_proto_timestamp")
        as_pb = _deprecation_decorator(as_protobuf, "utcnow.as_pb")
        to_protobuf = _deprecation_decorator(as_protobuf, "utcnow.to_protobuf")
        to_proto = _deprecation_decorator(as_protobuf, "utcnow.to_proto")
        to_protobuf_timestamp = _deprecation_decorator(as_protobuf, "utcnow.to_protobuf_timestamp")
        to_proto_timestamp = _deprecation_decorator(as_protobuf, "utcnow.to_proto_timestamp")
        to_pb = _deprecation_decorator(as_protobuf, "utcnow.to_pb")
        get_protobuf = _deprecation_decorator(as_protobuf, "utcnow.get_protobuf")
        get_proto = _deprecation_decorator(as_protobuf, "utcnow.get_proto")
        get_protobuf_timestamp = _deprecation_decorator(as_protobuf, "utcnow.get_protobuf_timestamp")
        get_proto_timestamp = _deprecation_decorator(as_protobuf, "utcnow.get_proto_timestamp")
        get_pb = _deprecation_decorator(as_protobuf, "utcnow.get_pb")
        proto = _deprecation_decorator(as_protobuf, "utcnow.proto")
        protobuf_timestamp = _deprecation_decorator(as_protobuf, "utcnow.protobuf_timestamp")
        proto_timestamp = _deprecation_decorator(as_protobuf, "utcnow.proto_timestamp")
        pb = _deprecation_decorator(as_protobuf, "utcnow.pb")

        time_diff = _deprecation_decorator(timediff, "utcnow.time_diff")
        diff = _deprecation_decorator(timediff, "utcnow.diff")
        timedelta = _deprecation_decorator(timediff, "utcnow.timedelta")
        delta = _deprecation_decorator(timediff, "utcnow.delta")

        as_datestring = _deprecation_decorator(as_date_string, "utcnow.as_datestring")
        as_date_str = _deprecation_decorator(as_date_string, "utcnow.as_date_str")
        as_datestr = _deprecation_decorator(as_date_string, "utcnow.as_datestr")
        to_date_string = _deprecation_decorator(as_date_string, "utcnow.to_date_string")
        to_datestring = _deprecation_decorator(as_date_string, "utcnow.to_datestring")
        to_date_str = _deprecation_decorator(as_date_string, "utcnow.to_date_str")
        to_datestr = _deprecation_decorator(as_date_string, "utcnow.to_datestr")
        get_date_string = _deprecation_decorator(as_date_string, "utcnow.get_date_string")
        get_datestring = _deprecation_decorator(as_date_string, "utcnow.get_datestring")
        get_datestr = _deprecation_decorator(as_date_string, "utcnow.get_datestr")
        get_date_string = _deprecation_decorator(as_date_string, "utcnow.get_date_string")
        date_string = _deprecation_decorator(as_date_string, "utcnow.date_string")
        datestring = _deprecation_decorator(as_date_string, "utcnow.datestring")
        date_str = _deprecation_decorator(as_date_string, "utcnow.date_str")
        datestr = _deprecation_decorator(as_date_string, "utcnow.datestr")

        get_today = _deprecation_decorator(today, "utcnow.get_today")
        get_today_date = _deprecation_decorator(today, "utcnow.get_today_date")
        get_todays_date = _deprecation_decorator(today, "utcnow.get_todays_date")
        get_date_today = _deprecation_decorator(today, "utcnow.get_date_today")
        date_today = _deprecation_decorator(as_date_string, "utcnow.date_today")
        today_date = _deprecation_decorator(today, "utcnow.today_date")
        todays_date = _deprecation_decorator(today, "utcnow.todays_date")

        def __str__(self) -> str:
            return self.rfc3339_timestamp()

        def __repr__(self) -> str:
            return self.rfc3339_timestamp()

    def staticmethod_(func: CT) -> CT:
        return cast(CT, staticmethod(func))

    utcnow_type = type(
        "utcnow",
        (utcnow_,),
        {
            "str": _deprecation_decorator(utcnow_.rfc3339_timestamp, "utcnow.str"),
            "datetime": _deprecation_decorator(utcnow_.as_datetime, "utcnow.datetime"),
            "protobuf": _deprecation_decorator(utcnow_.as_protobuf, "utcnow.protobuf"),
        },
    )
    utcnow = now = utcnow_type()

    rfc3339_timestamp = utcnow.rfc3339_timestamp
    as_datetime = utcnow.as_datetime
    as_unixtime = utcnow.as_unixtime
    as_protobuf = utcnow.as_protobuf
    as_date_string = utcnow.as_date_string
    today = utcnow.today
    timediff = utcnow.timediff

    __all__ = [
        "__version__",
        "__version_info__",
        "__author__",
        "__email__",
        "rfc3339_timestamp",
        "as_datetime",
        "as_unixtime",
        "as_protobuf",
        "as_date_string",
        "today",
        "timediff",
        "utcnow",
        "now",
        "synchronizer",
    ]

    code = """\
def __repr__(self) -> str:
    try:
        return self.__dict__.get(self.__name__).__repr__()
    except AttributeError:
        return "<module>"

module = type(
    "module",
    (ModuleType_,),
    {
        "__repr__": __repr__,
        "__spec__": original_module.__spec__,
        "__path__": original_module.__path__,
        "__annotations__": original_module.__annotations__,
        "__file__": original_module.__file__,
        "__package__": original_module.__package__,
        "__original_module__": original_module,
        "__class__": ModuleType_,
        "__all__": original_module.__all__,
        "__call__": staticmethod_(utcnow.rfc3339_timestamp),
        "_is_numeric": staticmethod_(_is_numeric),
        "_timestamp_to_datetime": staticmethod_(_timestamp_to_datetime),
        "_transform_value": staticmethod_(_transform_value),
        "utcnow": utcnow,
        "now": utcnow,
        "NOW": NOW,
        "TODAY": TODAY,
        "synchronizer": synchronizer,
        **{
            attr: staticmethod_(getattr(utcnow, attr))
            for attr in dir(utcnow)
            if not any(
                (
                    attr.startswith("_"),
                    not callable(getattr(utcnow, attr)),
                    not isinstance(getattr(utcnow, attr), FunctionType),
                    "." in getattr(getattr(utcnow, attr), "__qualname__", "."),
                )
            )
        },
    },
)
module_ = module(original_module.__name__, original_module.__doc__)
"""

    original_module = sys.modules[__name__]  # noqa
    code_object = compile(code, "<string>", "exec")
    globals_: Dict[str, Any] = {
        "ModuleType_": ModuleType,
        "staticmethod_": staticmethod_,
        "utcnow": utcnow,
        "FunctionType": FunctionType,
        "original_module": original_module,
        "cast": cast,
        "_is_numeric": _is_numeric,
        "_timestamp_to_datetime": _timestamp_to_datetime,
        "_transform_value": _transform_value,
        "NOW": NOW,
        "TODAY": TODAY,
        "synchronizer": synchronizer,
        "__builtins__": {
            "type": type,
            "print": print,
            "globals": globals,
            "__build_class__": __build_class__,
            "dir": dir,
            "any": any,
            "callable": callable,
            "getattr": getattr,
            "isinstance": isinstance,
            "setattr": setattr,
        },
    }
    locals_: Dict[str, Any] = {}
    exec(code_object, globals_, locals_)
    module_ = cast(ModuleType, locals_["module_"])

    del globals_
    del locals_

    if original_module.__annotations__ and isinstance(original_module.__annotations__, dict):
        original_module.__annotations__.pop("globals_")
        original_module.__annotations__.pop("locals_")

    module_.__dict__.update(
        {
            **{k: v for k, v in original_module.__dict__.items() if k in module_.__all__},
            "__str__": original_module.__str__,
            "__repr__": original_module.__repr__,
        }
    )
    module_.__spec__ = original_module.__spec__
    module_.__path__ = original_module.__path__
    module_.__annotations__ = original_module.__annotations__
    module_.__doc__ = original_module.__doc__
    module_.__file__ = original_module.__file__
    module_.__name__ = original_module.__name__
    module_.__package__ = original_module.__package__

    if sys.modules[__name__] is original_module:
        sys.modules[__name__] = module_

del sys
del annotations
