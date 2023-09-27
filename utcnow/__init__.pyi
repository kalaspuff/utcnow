from __future__ import annotations

import functools
from datetime import datetime, tzinfo
from decimal import Decimal
from numbers import Real
from typing import Any, Generic, Optional, Type, TypeVar, Union

from utcnow.protobuf import TimestampProtobufMessage

from .__version_data__ import __version__, __version_info__

__author__: str = ...
__email__: str = ...

NOW: object = ...
TODAY: object = ...

def rfc3339_timestamp(
    value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
    modifier: Optional[Union[str, int, float]] = 0,
) -> str:
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

@functools.lru_cache(maxsize=128)
def _timestamp_to_datetime(value: str) -> datetime:
    """Transforms the input value to a datetime object.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.

    Returns:
        The transformed value as a datetime object.
    """

@functools.lru_cache(maxsize=128, typed=True)
def _transform_value(value: Union[str, datetime, object, int, float, Decimal, Real]) -> str:
    """Transforms the input value to a timestamp string in RFC3339 format.

    Args:
        value: A value representing a timestamp in any of the allowed input formats.

    Returns:
        The transformed value as a string in RFC3339 format.
    """

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

    def __new__(cls: Type[TimeSynchronizer[TS]]) -> TimeSynchronizer[TS]: ...
    def __init__(self) -> None: ...
    def __call__(
        self: TimeSynchronizer[TS],
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
    def __enter__(self: TimeSynchronizer[TS]) -> TimeSynchronizer[TS]:
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
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def datetime(self) -> datetime: ...
    @property
    def time(self) -> float: ...
    @property
    def time_ns(self) -> int: ...
    @property
    def frozen(self) -> bool: ...

class TimeSynchronizerResult(TimeSynchronizer[TS]):
    def __new__(cls: Type[TimeSynchronizerResult[TS]]) -> TimeSynchronizerResult[TS]: ...
    def __eq__(self, other: Any) -> bool:
        return (
            True
            if (
                other is Type[TimeSynchronizerResult[TS]]
                or other is TimeSynchronizer[TS]
                or other is Type[TimeSynchronizer[TS]]
                or other is TimeSynchronizerResult[TS]
                or other is TimeSynchronizerResult[TimeSynchronizer[TS]]
                or other is Type[TimeSynchronizerResult[TimeSynchronizer[TS]]]
            )
            else False
        )

class __synchronizer(TimeSynchronizer[TS], metaclass=type):
    pass

synchronizer = __synchronizer__ = synchronizer__ = __synchronizer.__new__(__synchronizer)

class utcnow(str):
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __new__(  # type: ignore
        cls,
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    def __call__(
        self,
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    @staticmethod
    def rfc3339_timestamp(
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    @staticmethod
    def now(
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    as_string = rfc3339_timestamp
    as_str = rfc3339_timestamp
    as_rfc3339 = rfc3339_timestamp
    to_string = rfc3339_timestamp
    to_str = rfc3339_timestamp
    to_rfc3339 = rfc3339_timestamp
    get_string = rfc3339_timestamp
    get_str = rfc3339_timestamp
    get_rfc3339 = rfc3339_timestamp
    get = rfc3339_timestamp
    string = rfc3339_timestamp
    str = rfc3339_timestamp
    rfc3339 = rfc3339_timestamp
    timestamp_rfc3339 = rfc3339_timestamp
    ts_rfc3339 = rfc3339_timestamp
    rfc3339_ts = rfc3339_timestamp
    utcnow_rfc3339 = rfc3339_timestamp
    rfc3339_utcnow = rfc3339_timestamp
    now_rfc3339 = rfc3339_timestamp
    rfc3339_now = rfc3339_timestamp
    get_now = rfc3339_timestamp

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
    date_string = as_date_string
    datestring = as_date_string
    date_str = as_date_string
    datestr = as_date_string

    get_today = today
    get_today_date = today
    get_todays_date = today
    get_date_today = today
    date_today = as_date_string
    today_date = today
    todays_date = today

    synchronizer = __synchronizer__

class now(str):
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __new__(  # type: ignore
        cls,
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    def __call__(
        self,
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    @staticmethod
    def rfc3339_timestamp(
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    @staticmethod
    def now(
        value: Union[str, datetime, object, int, float, Decimal, Real] = NOW,
        modifier: Optional[Union[str, int, float]] = 0,
    ) -> str:
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
    as_string = rfc3339_timestamp
    as_str = rfc3339_timestamp
    as_rfc3339 = rfc3339_timestamp
    to_string = rfc3339_timestamp
    to_str = rfc3339_timestamp
    to_rfc3339 = rfc3339_timestamp
    get_string = rfc3339_timestamp
    get_str = rfc3339_timestamp
    get_rfc3339 = rfc3339_timestamp
    get = rfc3339_timestamp
    string = rfc3339_timestamp
    str = rfc3339_timestamp
    rfc3339 = rfc3339_timestamp
    timestamp_rfc3339 = rfc3339_timestamp
    ts_rfc3339 = rfc3339_timestamp
    rfc3339_ts = rfc3339_timestamp
    utcnow_rfc3339 = rfc3339_timestamp
    rfc3339_utcnow = rfc3339_timestamp
    now_rfc3339 = rfc3339_timestamp
    rfc3339_now = rfc3339_timestamp
    get_now = rfc3339_timestamp

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
    date_string = as_date_string
    datestring = as_date_string
    date_str = as_date_string
    datestr = as_date_string

    get_today = today
    get_today_date = today
    get_todays_date = today
    get_date_today = today
    date_today = as_date_string
    today_date = today
    todays_date = today

    synchronizer = __synchronizer__

as_string = rfc3339_timestamp
as_str = rfc3339_timestamp
as_rfc3339 = rfc3339_timestamp
to_string = rfc3339_timestamp
to_str = rfc3339_timestamp
to_rfc3339 = rfc3339_timestamp
get_string = rfc3339_timestamp
get_str = rfc3339_timestamp
get_rfc3339 = rfc3339_timestamp
get = rfc3339_timestamp
string = rfc3339_timestamp
rfc3339 = rfc3339_timestamp
timestamp_rfc3339 = rfc3339_timestamp
ts_rfc3339 = rfc3339_timestamp
rfc3339_ts = rfc3339_timestamp
utcnow_rfc3339 = rfc3339_timestamp
rfc3339_utcnow = rfc3339_timestamp
now_rfc3339 = rfc3339_timestamp
rfc3339_now = rfc3339_timestamp
get_now = rfc3339_timestamp

as_date = as_datetime
as_dt = as_datetime
to_datetime = as_datetime
to_date = as_datetime
to_dt = as_datetime
get_datetime = as_datetime
get_date = as_datetime
get_dt = as_datetime
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
date_string = as_date_string
datestring = as_date_string
date_str = as_date_string
datestr = as_date_string

get_today = today
get_today_date = today
get_todays_date = today
get_date_today = today
date_today = as_date_string
today_date = today
todays_date = today

__all__ = [
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "utcnow",
    "now",
    "as_date_string",
    "as_datetime",
    "as_protobuf",
    "as_unixtime",
    "rfc3339_timestamp",
    "timediff",
    "today",
    "synchronizer",
    "_is_numeric",
    "_timestamp_to_datetime",
    "_transform_value",
]
