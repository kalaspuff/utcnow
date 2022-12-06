import datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp


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
        assert isinstance(utcnow.as_unixtime(value), (float, int))
        assert isinstance(utcnow.as_protobuf(value), Timestamp)
        if expect_error:
            assert False
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
    assert utcnow.utcnow(utcnow.as_datetime(value)) == utcnow.utcnow(utcnow.as_datetime(expected_output))
    assert utcnow.utcnow(utcnow.as_datetime(value).replace(tzinfo=None)) == expected_output
    assert utcnow.as_string(utcnow.utcnow(utcnow.as_datetime(value))) == expected_output
