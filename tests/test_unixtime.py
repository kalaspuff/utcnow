import datetime
from decimal import Decimal
from typing import Union

import pytest


@pytest.mark.parametrize(
    "value, expected_output, expect_error",
    [
        (0, "1970-01-01T00:00:00.000000Z", False),
        (0.0, "1970-01-01T00:00:00.000000Z", False),
        (0.000000, "1970-01-01T00:00:00.000000Z", False),
        (0.000001, "1970-01-01T00:00:00.000001Z", False),
        (0.000001, "1970-01-01T00:00:00.000001Z", False),
        (0.01, "1970-01-01T00:00:00.010000Z", False),
        (1, "1970-01-01T00:00:01.000000Z", False),
        (1.0, "1970-01-01T00:00:01.000000Z", False),
        (1338, "1970-01-01T00:22:18.000000Z", False),
        (4711 * 3.14, "1970-01-01T04:06:32.540000Z", False),
        ("0", "1970-01-01T00:00:00.000000Z", False),
        ("0.00", "1970-01-01T00:00:00.000000Z", False),
        ("0.000109", "1970-01-01T00:00:00.000109Z", False),
        (".000109", "1970-01-01T00:00:00.000109Z", False),
        ("1614300199.462145", "2021-02-26T00:43:19.462145Z", False),
        ("1614300199.", "2021-02-26T00:43:19.000000Z", False),
        (".9919", "1970-01-01T00:00:00.991900Z", False),
        ("-0", "1970-01-01T00:00:00.000000Z", False),
        ("-1", "1969-12-31T23:59:59.000000Z", False),
        ("-0.000109", "1969-12-31T23:59:59.999891Z", False),
        ("-.000109", "1969-12-31T23:59:59.999891Z", False),
        ("-1614300199.462145", "1918-11-05T23:16:40.537855Z", False),
        ("-1614300199.", "1918-11-05T23:16:41.000000Z", False),
        ("-.9919", "1969-12-31T23:59:59.008100Z", False),
        (0, "1970-01-01T00:00:00.000000Z", False),
        (0.00, "1970-01-01T00:00:00.000000Z", False),
        (0.000109, "1970-01-01T00:00:00.000109Z", False),
        (0.000109, "1970-01-01T00:00:00.000109Z", False),
        (1614300199.462145, "2021-02-26T00:43:19.462145Z", False),
        (1614300199.0, "2021-02-26T00:43:19.000000Z", False),
        (0.9919, "1970-01-01T00:00:00.991900Z", False),
        (-0, "1970-01-01T00:00:00.000000Z", False),
        (-1, "1969-12-31T23:59:59.000000Z", False),
        (-0.000109, "1969-12-31T23:59:59.999891Z", False),
        (-0.000109, "1969-12-31T23:59:59.999891Z", False),
        (-1614300199.462145, "1918-11-05T23:16:40.537855Z", False),
        (-1614300199.0, "1918-11-05T23:16:41.000000Z", False),
        (-0.9919, "1969-12-31T23:59:59.008100Z", False),
        (Decimal("0"), "1970-01-01T00:00:00.000000Z", False),
        (Decimal("-0"), "1970-01-01T00:00:00.000000Z", False),
        (Decimal("0.00"), "1970-01-01T00:00:00.000000Z", False),
        (Decimal("0.000109"), "1970-01-01T00:00:00.000109Z", False),
        (Decimal(".000109"), "1970-01-01T00:00:00.000109Z", False),
        (Decimal("1614300199.462145"), "2021-02-26T00:43:19.462145Z", False),
        (Decimal("1614300199."), "2021-02-26T00:43:19.000000Z", False),
        (Decimal(".9919"), "1970-01-01T00:00:00.991900Z", False),
        (Decimal("-0"), "1970-01-01T00:00:00.000000Z", False),
        (Decimal("-1"), "1969-12-31T23:59:59.000000Z", False),
        (Decimal("-0.000109"), "1969-12-31T23:59:59.999891Z", False),
        (Decimal("-.000109"), "1969-12-31T23:59:59.999891Z", False),
        (Decimal("-1614300199.462145"), "1918-11-05T23:16:40.537855Z", False),
        (Decimal("-1614300199."), "1918-11-05T23:16:41.000000Z", False),
        (Decimal("-.9919"), "1969-12-31T23:59:59.008100Z", False),
        (Decimal("5e5"), "1970-01-06T18:53:20.000000Z", False),
        ("1.0.0", "", True),
        ("--1", "", True),
        ("--", "", True),
        ("-", "", True),
        (".", "", True),
        (".-1", "", True),
        ("1..", "", True),
        ("..1", "", True),
        ("..1", "", True),
        (float("inf"), "", True),
        (Decimal("Infinity"), "", True),
        (Decimal("1e100"), "", True),
        (Decimal("-1e100"), "", True),
    ],
)
def test_unixtime_values(value: Union[int, float, str, Decimal], expected_output: str, expect_error: bool) -> None:
    import utcnow

    try:
        assert isinstance(utcnow.as_string(value), str)
        assert isinstance(utcnow.as_datetime(value), datetime.datetime)
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
