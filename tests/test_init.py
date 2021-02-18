import datetime
import json

import pytest


def test_init() -> None:
    import utcnow
    from utcnow import __version__, __version_info__

    assert utcnow

    assert isinstance(utcnow.__version_info__, tuple)
    assert utcnow.__version_info__
    assert isinstance(utcnow.__version__, str)
    assert len(utcnow.__version__)

    assert isinstance(__version_info__, tuple)
    assert __version_info__
    assert isinstance(__version__, str)
    assert len(__version__)

    from utcnow.__version__ import __version__ as __version2__, __version_info__ as __version_info2__  # isort:skip

    assert isinstance(__version_info2__, tuple)
    assert __version_info2__
    assert isinstance(__version2__, str)
    assert len(__version2__)


def test_module() -> None:
    import utcnow

    # Test types
    assert type(utcnow) is utcnow._module
    assert len(str(utcnow)) == 27
    assert isinstance(repr(utcnow), str)
    assert len(repr(utcnow)) == 27

    # Modules aren't callable, but this one is – it's frowned upon and bad practice.
    assert utcnow("1984-08-01") == "1984-08-01T00:00:00.000000Z"  # type: ignore
    assert utcnow("1984-08-01 00:00:00") == "1984-08-01T00:00:00.000000Z"  # type: ignore
    assert utcnow("1984-08-01 12:00:00") != "1984-08-01T00:00:00.000000Z"  # type: ignore
    assert datetime.datetime.strptime(utcnow(), "%Y-%m-%dT%H:%M:%S.%f%z")  # type: ignore
    assert datetime.datetime.strptime(str(utcnow), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert utcnow(datetime.datetime(2021, 4, 30, 8, 0)) == "2021-04-30T08:00:00.000000Z"  # type: ignore

    # Testing module functions
    assert utcnow.utcnow("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow("1984-08-01 00:00:00") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow("1984-08-01 12:00:00") != "1984-08-01T00:00:00.000000Z"
    assert utcnow.as_string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.as_str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow.as_string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow.as_str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow.string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow.utcnow.str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert datetime.datetime.strptime(utcnow.utcnow(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.as_string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.as_str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.utcnow.as_string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.utcnow.as_str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.utcnow.string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow.utcnow.str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(str(utcnow.utcnow), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert utcnow.utcnow(datetime.datetime(2021, 4, 30, 8, 0)) == "2021-04-30T08:00:00.000000Z"
    assert utcnow.as_datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.utcnow.as_datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.utcnow.as_date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.utcnow.datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow.utcnow.date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )

    # Timezone test
    assert utcnow.as_datetime("2021-04-30T09:00:00.000000+01:00") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000+00:00") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000-00:00") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T07:00:00.000000-01:00") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000 UTC") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000") == datetime.datetime(
        2021, 4, 30, 8, 0, tzinfo=datetime.timezone.utc
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000 UTC") != datetime.datetime(2021, 4, 30, 8, 0)
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000 UTC") == utcnow.as_datetime(
        datetime.datetime(2021, 4, 30, 8, 0)
    )
    assert utcnow.as_datetime("2021-04-30T08:00:00.000000 UTC") != utcnow.as_datetime(
        datetime.datetime(2021, 4, 30, 8, 1)
    )
    assert utcnow.as_string(utcnow.as_datetime("2021-04-30T08:00:00.000000 UTC")) == utcnow.utcnow(
        utcnow.as_datetime(datetime.datetime(2021, 4, 30, 8, 0))
    )

    # Testing function imports
    from utcnow import as_str, as_string
    from utcnow import str as str_
    from utcnow import string

    assert as_string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert as_str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert str_("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert datetime.datetime.strptime(as_string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(as_str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(str_(), "%Y-%m-%dT%H:%M:%S.%f%z")

    # Testing submodule import with function calls
    from utcnow import utcnow as utcnow_

    assert utcnow_("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow_.as_string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow_.as_str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow_.string("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert utcnow_.str("1984-08-01") == "1984-08-01T00:00:00.000000Z"
    assert datetime.datetime.strptime(utcnow_(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow_.as_string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow_.as_str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow_.string(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(utcnow_.str(), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert datetime.datetime.strptime(str(utcnow_), "%Y-%m-%dT%H:%M:%S.%f%z")
    assert utcnow_(datetime.datetime(2021, 4, 30, 8, 0)) == "2021-04-30T08:00:00.000000Z"
    assert utcnow_.as_datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow_.as_date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow_.datetime("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )
    assert utcnow_.date("2021-04-30T08:00:10.000000Z") == datetime.datetime(
        2021, 4, 30, 8, 0, 10, tzinfo=datetime.timezone.utc
    )


@pytest.mark.parametrize(
    "value, expected_output, expect_error",
    [
        # This represents 20 minutes and 50.52 seconds after the 23rd hour of April 12th, 1985 in UTC.
        ("1985-04-12T23:20:50.52Z", "1985-04-12T23:20:50.520000Z", False),
        # This represents 39 minutes and 57 seconds after the 16th hour of December 19th, 1996 with an offset of
        # -08:00 from UTC (Pacific Standard Time).  Note that this is equivalent to 1996-12-20T00:39:57Z in UTC.
        ("1996-12-19T16:39:57-08:00", "1996-12-20T00:39:57.000000Z", False),
        # This represents the same instant of time as noon, January 1, 1937, Netherlands time. Standard time in the
        # Netherlands was exactly 19 minutes and 32.13 seconds ahead of UTC by law from 1909-05-01 through 1937-06-30.
        ("1937-01-01T12:00:27.87+00:20", "1937-01-01T11:40:27.870000Z", False),
        # This represents the leap second inserted at the end of 1990. However this will fail since we can't handle
        # second number 60.
        ("1990-12-31T15:59:60-08:00", "1990-12-31T23:59:60.000000Z", True),
        # Other tests for allowed input formats
        ("2021-02-18", "2021-02-18T00:00:00.000000Z", False),
        ("2021-02-18 01:00", "2021-02-18T01:00:00.000000Z", False),
        ("2021-02-18 03:00+01:00", "2021-02-18T02:00:00.000000Z", False),
        ("2021-02-18-01:00", "2021-02-18T01:00:00.000000Z", False),
        ("2021-02-18+01:00", "2021-02-17T23:00:00.000000Z", False),
        ("2021-02-18T23:55", "2021-02-18T23:55:00.000000Z", False),
        ("2021-02-18T23:55:10", "2021-02-18T23:55:10.000000Z", False),
        ("2021-02-18T23:55:10.0", "2021-02-18T23:55:10.000000Z", False),
        ("2021-02-18T23:55:10.0+05:00", "2021-02-18T18:55:10.000000Z", False),
        ("2021-02-18T23:55:10.0-05:00", "2021-02-19T04:55:10.000000Z", False),
        ("2021-02-18T23:55:10.550-05:00", "2021-02-19T04:55:10.550000Z", False),
        ("2021-02-18 23:55:10.550+05:00", "2021-02-18T18:55:10.550000Z", False),
        ("2021-02-18 23:55:10.550-01:00", "2021-02-19T00:55:10.550000Z", False),
        ("2021-02-28 10:10:59.123987+00:00", "2021-02-28T10:10:59.123987Z", False),
        ("2021-02-28 10:10:59.123987Z", "2021-02-28T10:10:59.123987Z", False),
        ("2021-02-28 10:10:59.123987 UTC", "2021-02-28T10:10:59.123987Z", False),
        # Not allowed input formats
        ("2021-02-28 10:10:59.123987+00:00 UTC", "", True),
        ("2021-02-28 10:10:59.123987 Europe/Stockholm", "", True),
        ("2021/02/28", "", True),
        ("21-02-28 10:10:59.123987+00:00", "", True),
        ("2021", "", True),
        ("2021-02", "", True),
        ("2021-02-30", "", True),
        ("1900-01-01 20:30.123", "", True),
    ],
)
def test_to_string_values(value: str, expected_output: str, expect_error: bool) -> None:
    import utcnow

    try:
        assert isinstance(utcnow.as_string(value), str)
        assert isinstance(utcnow.as_datetime(value), datetime.datetime)
    except Exception:
        if not expect_error:
            raise
        if not expect_error:
            # unreachable
            assert False

        assert True
        return

    assert utcnow.as_string(value) == expected_output
    assert utcnow.as_string(expected_output) == expected_output
    assert utcnow.as_string(expected_output) == utcnow.as_string(expected_output)
    assert utcnow.as_datetime(value) == utcnow.as_datetime(expected_output)


def test_fstring() -> None:
    import utcnow

    result = f"Current server time is {utcnow}"
    assert result.count("-") == 2
    assert result.count(":") == 2
    assert result.count("T") == 1
    assert result.count("Z") == 1
    assert result.endswith("Z")
    assert "Current server time is 2" in result

    result = f"Current server time is {utcnow.utcnow}"
    assert result.count("-") == 2
    assert result.count(":") == 2
    assert result.count("T") == 1
    assert result.count("Z") == 1
    assert result.endswith("Z")
    assert "Current server time is 2" in result


def test_as_reference() -> None:
    import utcnow

    dict1 = {"timestamp": str(utcnow)}
    a = str(dict1)
    b = str(dict1)
    assert a == b

    dict2 = {"timestamp": utcnow}
    a = str(dict2)
    b = str(dict2)
    assert a != b


def test_json() -> None:
    import utcnow

    result = json.dumps({"timestamp": str(utcnow)}).encode()
    assert utcnow.as_string(json.loads(result).get("timestamp")) == json.loads(result).get("timestamp")

    with pytest.raises(TypeError):
        json.dumps({"timestamp": utcnow})
