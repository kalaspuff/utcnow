import utcnow


def test_rfc3339_modifier() -> None:
    assert utcnow.rfc3339_timestamp("2022-10-17T15:15:22.556084Z", "+365d") == "2023-10-17T15:15:22.556084Z"
    assert utcnow.rfc3339_timestamp("2022-10-17T15:15:22.556084Z", ".4") == "2022-10-17T15:15:22.956084Z"
    assert utcnow.rfc3339_timestamp(1666019834.321119, "-10s") == "2022-10-17T15:17:04.321119Z"


def test_unxitime_modifier() -> None:
    assert utcnow.unixtime(0, "+10s") == 10.0
    assert utcnow.unixtime(0, "+24h") == 86400.0
    assert utcnow.unixtime("now", None) < utcnow.unixtime("+1s")
    assert utcnow.unixtime("2022-10-17T15:15:22.556084Z", None) == utcnow.unixtime("2022-10-17T15:15:22.556084Z", 0) == utcnow.unixtime("2022-10-17T15:15:22.556084Z")


def test_unixtime_modifier() -> None:
    assert utcnow.as_datetime("now", "+60s") > utcnow.as_datetime("now")
    assert utcnow.as_datetime("+60s") > utcnow.as_datetime("now")
    assert utcnow.as_datetime("-60s") < utcnow.as_datetime("now")
