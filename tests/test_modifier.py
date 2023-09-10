from datetime import UTC, datetime

from freezegun import freeze_time

import utcnow


def test_rfc3339_modifier() -> None:
    assert utcnow.rfc3339_timestamp(0, "+7d") == "1970-01-08T00:00:00.000000Z"
    assert utcnow.rfc3339_timestamp("2022-10-17T15:15:22.556084Z", "+365d") == "2023-10-17T15:15:22.556084Z"
    assert utcnow.rfc3339_timestamp("2022-10-17T15:15:22.556084Z", ".4") == "2022-10-17T15:15:22.956084Z"
    assert utcnow.rfc3339_timestamp(1666019834.321119, "-10s") == "2022-10-17T15:17:04.321119Z"


def test_unixtime_modifier() -> None:
    assert utcnow.unixtime(0, "+7d") == 604800.0
    assert utcnow.unixtime(0, "+10s") == 10.0
    assert utcnow.unixtime(0, "+24h") == 86400.0
    assert utcnow.unixtime("now", None) < utcnow.unixtime("+1s")
    assert (
        utcnow.unixtime("2022-10-17T15:15:22.556084Z", None)
        == utcnow.unixtime("2022-10-17T15:15:22.556084Z", 0)
        == utcnow.unixtime("2022-10-17T15:15:22.556084Z")
    )


def test_datetime_modifier() -> None:
    assert utcnow.as_datetime(0, "+7d") == datetime(1970, 1, 8, 0, 0, 0, 0, tzinfo=UTC)
    assert utcnow.as_datetime("now", "+60s") > utcnow.as_datetime("now")
    assert utcnow.as_datetime("+60s") > utcnow.as_datetime("now")
    assert utcnow.as_datetime("-60s") < utcnow.as_datetime("now")


def test_protobuf_modifier() -> None:
    assert utcnow.unixtime(utcnow.as_protobuf(0, "+10s")) == 10.0
    assert utcnow.unixtime(utcnow.as_protobuf(0, "+24h")) == 86400.0
    assert utcnow.as_datetime(utcnow.as_protobuf("now", None)) < utcnow.as_datetime(utcnow.as_protobuf("+1s"))
    assert (
        utcnow.as_protobuf("2022-10-17T15:15:22.556084Z", None)
        == utcnow.as_protobuf("2022-10-17T15:15:22.556084Z", 0)
        == utcnow.as_protobuf("2022-10-17T15:15:22.556084Z")
    )
    assert utcnow.unixtime(utcnow.as_protobuf("+10s")) > utcnow.unixtime()
    assert utcnow.unixtime(utcnow.as_protobuf("-10s")) < utcnow.unixtime()


def test_sentinel_modifier() -> None:
    with freeze_time("1970-01-01"):
        assert utcnow.rfc3339_timestamp() == utcnow.rfc3339_timestamp()
        assert utcnow.unixtime() == utcnow.unixtime()
        assert utcnow.as_datetime() == utcnow.as_datetime()
        assert utcnow.as_protobuf() == utcnow.as_protobuf()
        assert utcnow.rfc3339_timestamp(0) == utcnow.rfc3339_timestamp()
        assert utcnow.unixtime(0) == utcnow.unixtime()
        assert utcnow.as_datetime(0) == utcnow.as_datetime()
        assert utcnow.as_protobuf(0) == utcnow.as_protobuf()
        assert utcnow.rfc3339_timestamp("+1s") > utcnow.rfc3339_timestamp()
        assert utcnow.unixtime("+1s") == utcnow.unixtime() + 1
        assert utcnow.as_datetime("+1s") > utcnow.as_datetime()
        assert utcnow.as_protobuf("+1s").seconds == 1
        assert utcnow.as_protobuf("+1s").nanos == 0
        assert utcnow.as_protobuf("-1s").seconds == -1
        assert utcnow.unixtime(utcnow.as_protobuf("+10s")) == 10.0
        assert utcnow.unixtime(utcnow.as_protobuf("+24h")) == 86400.0
        assert utcnow.unixtime(utcnow.as_protobuf("-10s")) == -10
        assert utcnow.rfc3339_timestamp(utcnow.as_protobuf("-10s")) == "1969-12-31T23:59:50.000000Z"
        assert utcnow.rfc3339_timestamp(utcnow.as_protobuf("-10s")) < utcnow.rfc3339_timestamp()
        assert utcnow.unixtime(utcnow.as_protobuf("-10s")) < utcnow.unixtime()
        assert utcnow.rfc3339_timestamp(utcnow.as_protobuf("+1.123987s")) == "1970-01-01T00:00:01.123987Z"
        assert utcnow.rfc3339_timestamp(utcnow.as_protobuf("-1.123987s")) == "1969-12-31T23:59:58.876013Z"
        assert utcnow.rfc3339_timestamp(utcnow.as_protobuf("-0.4711s")) == "1969-12-31T23:59:59.528900Z"
