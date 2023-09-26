from typing import Any, cast

import pytest

import utcnow


def test_synchronizer_basic() -> None:
    with utcnow.synchronizer as synchronizer:
        assert utcnow.rfc3339_timestamp() == utcnow.rfc3339_timestamp("now")
        assert utcnow.as_unixtime() == utcnow.as_unixtime("now")
        assert utcnow.as_protobuf() == utcnow.as_protobuf("now")
        assert utcnow.as_datetime() == utcnow.as_datetime("now")

        assert synchronizer.datetime == utcnow.as_datetime()
        assert synchronizer.time == utcnow.as_unixtime()
        assert synchronizer.time_ns == int(utcnow.as_unixtime() * 1e6) * 1_000

    with utcnow.utcnow.synchronizer as synchronizer:
        assert utcnow.rfc3339_timestamp() == utcnow.rfc3339_timestamp("now")
        assert utcnow.as_unixtime() == utcnow.as_unixtime("now")
        assert utcnow.as_protobuf() == utcnow.as_protobuf("now")
        assert utcnow.as_datetime() == utcnow.as_datetime("now")

        assert synchronizer.datetime == utcnow.as_datetime()
        assert synchronizer.time == utcnow.as_unixtime()
        assert synchronizer.time_ns == int(utcnow.as_unixtime() * 1e6) * 1_000


def test_synchronizer_timediff() -> None:
    assert utcnow.timediff("now", "now") == 0.0
    assert utcnow.timediff("now", "+1h") == 3600.0
    assert utcnow.timediff("-1h", "+0.5h") == 5400.0

    with utcnow.synchronizer:
        assert utcnow.timediff("now", "now") == 0.0
        assert utcnow.timediff("now", "+1h") == 3600.0
        assert utcnow.timediff("-1h", "+0.5h") == 5400.0

    with utcnow.synchronizer("1984-08-01 20:50:33.414100+02:00"):
        assert utcnow.timediff("now", "now") == 0.0
        assert utcnow.timediff("now", "+1h") == 3600.0
        assert utcnow.timediff("-1h", "+0.5h") == 5400.0


def test_synchronizer_now() -> None:
    with utcnow.synchronizer:
        created_time = utcnow.rfc3339_timestamp()
        expire_time = utcnow.rfc3339_timestamp("now", "+15m")

    assert utcnow.timediff(created_time, expire_time, "seconds") == 900.0


def test_synchronizer_specific() -> None:
    with utcnow.synchronizer("2022-01-01T01:00:00.000000Z") as synchronizer:
        created_time = utcnow.rfc3339_timestamp()
        expire_time = utcnow.rfc3339_timestamp("now", "+15m")

        assert synchronizer.datetime == utcnow.as_datetime()
        assert synchronizer.time == utcnow.as_unixtime()
        assert synchronizer.time_ns == int(utcnow.as_unixtime() * 1e6) * 1_000

    assert utcnow.timediff(created_time, expire_time, "seconds") == 900.0
    assert created_time == "2022-01-01T01:00:00.000000Z"
    assert expire_time == "2022-01-01T01:15:00.000000Z"


def test_synchronizer_precise_unixtime() -> None:
    with utcnow.synchronizer(1695694079.9417229) as synchronizer:
        created_time = utcnow.rfc3339_timestamp()
        expire_time = utcnow.rfc3339_timestamp("now", "+15m")

        assert synchronizer.datetime == utcnow.as_datetime()
        assert synchronizer.time == utcnow.as_unixtime()
        assert synchronizer.time_ns == int(utcnow.as_unixtime() * 1e6) * 1_000

        assert synchronizer.time == 1695694079.941723
        assert synchronizer.time_ns == 1695694079941723000

    assert utcnow.timediff(created_time, expire_time, "seconds") == 900.0
    assert created_time == "2023-09-26T02:07:59.941723Z"
    assert expire_time == "2023-09-26T02:22:59.941723Z"


def test_synchronizer_approximate_unixtime() -> None:
    with utcnow.synchronizer(1695694079.941723) as synchronizer:
        created_time = utcnow.rfc3339_timestamp()
        expire_time = utcnow.rfc3339_timestamp("now", "+15m")

        assert synchronizer.datetime == utcnow.as_datetime()
        assert synchronizer.time == utcnow.as_unixtime()
        assert synchronizer.time_ns == int(utcnow.as_unixtime() * 1e6) * 1_000

        assert synchronizer.time == 1695694079.941723
        assert synchronizer.time_ns == 1695694079941723000

    assert utcnow.timediff(created_time, expire_time, "seconds") == 900.0
    assert created_time == "2023-09-26T02:07:59.941723Z"
    assert expire_time == "2023-09-26T02:22:59.941723Z"


def test_synchronizer_only_modifier() -> None:
    now = utcnow.rfc3339_timestamp()

    with utcnow.synchronizer(utcnow.NOW, "+1h"):
        timestamp = utcnow.rfc3339_timestamp()

    assert 3601.0 > utcnow.timediff(now, timestamp, "seconds") >= 3600.0

    with utcnow.synchronizer("-10s"):
        timestamp = utcnow.rfc3339_timestamp()

    assert -10.0 < utcnow.timediff(now, timestamp, "seconds") < -9.0


def test_synchronizer_expired() -> None:
    synchronizer1 = utcnow.synchronizer("2022-01-01T01:00:00.000000Z")
    synchronizer2 = utcnow.synchronizer("2022-01-01T02:00:00.000000Z")
    assert synchronizer1 is not synchronizer2

    assert "expired" in repr(synchronizer1)
    assert "pending context" in repr(synchronizer2)

    with pytest.raises(RuntimeError):
        with synchronizer1 as synchronizer:
            pass

    assert utcnow.rfc3339_timestamp() != "2022-01-01T02:00:00.000000Z"

    with synchronizer2 as synchronizer:
        assert utcnow.rfc3339_timestamp() == "2022-01-01T02:00:00.000000Z"
        assert synchronizer is utcnow.synchronizer

    assert utcnow.rfc3339_timestamp() != "2022-01-01T02:00:00.000000Z"

    with pytest.raises(RuntimeError):
        with synchronizer2 as synchronizer:
            pass


def test_synchronizer_reuse() -> None:
    synchronizer = cast(Any, utcnow.synchronizer("2022-01-01T01:00:00.000000Z"))

    with pytest.raises(RuntimeError):
        synchronizer("2022-01-01T01:00:00.000000Z")


def test_synchronizer_repr() -> None:
    synchronizer1 = utcnow.synchronizer()

    assert "pending context" in repr(synchronizer1)
    assert "pending context" not in repr(utcnow.synchronizer)

    with synchronizer1 as synchronizer:
        assert synchronizer is utcnow.synchronizer
        assert synchronizer == utcnow.synchronizer
        assert synchronizer is not synchronizer1
        assert synchronizer != synchronizer1
        assert "child" in repr(synchronizer1)
        assert "active context" in repr(synchronizer1)
        assert "main" in repr(synchronizer)
        assert "active context" in repr(synchronizer)

    assert "active context" not in repr(synchronizer1)
    assert "active context" not in repr(synchronizer)
    assert "deactivated context" in repr(synchronizer1)

    with pytest.raises(RuntimeError):
        with synchronizer1:
            pass


def test_synchronizer_orphan() -> None:
    synchronizer1 = utcnow.synchronizer("+10h")

    assert "pending context" in repr(synchronizer1)
    assert "pending context" not in repr(utcnow.synchronizer)

    with utcnow.synchronizer as synchronizer:
        assert synchronizer is utcnow.synchronizer
        assert synchronizer is not synchronizer1
        assert "child" in repr(synchronizer1)
        assert "expired" in repr(synchronizer1)
        assert "main" in repr(synchronizer)
        assert "active context" in repr(synchronizer)

    assert "expired" in repr(synchronizer1)

    with pytest.raises(RuntimeError):
        with synchronizer1:
            pass


def test_synchronizer_nested() -> None:
    with utcnow.synchronizer("2022-01-01T01:00:00.000000Z"):
        with pytest.raises(RuntimeError):
            with utcnow.synchronizer:
                pass

    with utcnow.synchronizer:
        with pytest.raises(RuntimeError):
            with utcnow.synchronizer:
                pass

        with pytest.raises(RuntimeError):
            utcnow.synchronizer()
