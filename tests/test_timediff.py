import pytest


def test_timediff_basic() -> None:
    import utcnow

    assert utcnow.timediff(0, 0) == 0
    assert utcnow.timediff(0, 1) == 1
    assert utcnow.timediff(1, 0) == -1
    assert utcnow.timediff(0, -1) == -1
    assert utcnow.timediff(begin=0, end=1) == 1
    assert utcnow.timediff(end=1, begin=0) == 1
    assert utcnow.timediff(0, 2) == 2
    assert utcnow.timediff(0, 60) == 60
    assert utcnow.timediff(0, 4.711, "milliseconds") == 4711.0
    assert utcnow.timediff(0, 0.013338, "microseconds") == 13338.0
    assert utcnow.timediff(0, 0.000042, "nanoseconds") == 42000.0
    assert utcnow.timediff(0, 60, "seconds") == 60
    assert utcnow.timediff(0, 60, "minutes") == 1
    assert utcnow.timediff(0, 60 * 60, "minutes") == 60
    assert utcnow.timediff(0, 60 * 60, "hours") == 1
    assert utcnow.timediff(0, 60 * 60 * 24, "hours") == 24
    assert utcnow.timediff(0, 60 * 60 * 24, "days") == 1
    assert utcnow.timediff(0, 60 * 60 * 24 * 7, "days") == 7
    assert utcnow.timediff(0, 60 * 60 * 24 * 7, "weeks") == 1
    assert utcnow.timediff(0, 60 * 60 * 24 * 7 * 4, "days") == 28
    assert utcnow.timediff(0, 60 * 60 * 24 * 7 * 4, "weeks") == 4


def test_timediff_comparison() -> None:
    import utcnow

    assert utcnow.timediff("1984-08-01", "1984-08-01") == 0

    assert utcnow.timediff("1984-08-01", "1984-08-02") == 86400
    assert utcnow.timediff("1984-08-01", "1984-08-02", "minutes") == 1440
    assert utcnow.timediff("1984-08-01", "1984-08-02", "hours") == 24
    assert utcnow.timediff("1984-08-01", "1984-08-02", "days") == 1

    assert utcnow.timediff("1984-08-01", "1984-08-02 00:00:30") == 86430
    assert utcnow.timediff("1984-08-01", "1984-08-02 00:00:30", "minutes") == 1440.5
    assert round(utcnow.timediff("1984-08-01", "1984-08-02 00:00:30", "hours"), 8) == round(24.00833333333333333333, 8)
    assert round(utcnow.timediff("1984-08-01", "1984-08-02 00:00:30", "days"), 8) == round(1.00034722222222222222, 8)

    assert utcnow.timediff("1984-08-01T00:50:15", "1984-08-02") == 83385.0
    assert utcnow.timediff("1984-08-01T00:50:15", "1984-08-02", "minutes") == 1389.75
    assert round(utcnow.timediff("1984-08-01T00:50:15", "1984-08-02", "hours"), 8) == round(23.1625, 8)
    assert round(utcnow.timediff("1984-08-01T00:50:15", "1984-08-02", "days"), 8) == round(0.96510417, 8)

    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:00.471101Z") == 0.000001
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:00.471101Z", "ms") == 0.001
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:00.471101Z", "us") == 1.0
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01") == 0.528900
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000Z") == 0.528900
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000+00:00") == 0.528900
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000+01:00") == -3599.4711
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000+01:00", "hours") < 1
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000-01:00") == 3600.5289
    assert utcnow.timediff("1984-08-01T13:38:00.471100Z", "1984-08-01T13:38:01.000000-01:00", "hours") > 1

    assert utcnow.timediff("2020-02-01", "2020-03-01") == 60 * 60 * 24 * 29
    assert utcnow.timediff("2020-02-01", "2020-03-01", "days") == 29
    assert utcnow.timediff("2021-02-01", "2021-03-01") == 60 * 60 * 24 * 28
    assert utcnow.timediff("2021-02-01", "2021-03-01", "days") == 28
    assert round(utcnow.timediff("2020-02-01", "2020-03-01", "weeks"), 8) == round(4.142857142857143, 8)
    assert utcnow.timediff("2021-02-01", "2021-03-01", "weeks") == 4

    # year of covid-19, was longer than usual, felt way longer
    assert utcnow.timediff("2020-01-01", "2021-01-01", "days") == 366

    assert utcnow.timediff("2021-01-01", "2022-01-01", "days") == 365


def test_timediff_birth() -> None:
    import utcnow

    begin = "1984-08-01T13:38:00.471100Z"
    end = "2021-02-27T08:54:30.999999Z"

    assert utcnow.timediff(begin, end) == utcnow.timediff(utcnow.get(begin), utcnow.get(end))
    assert utcnow.timediff(begin, end) == utcnow.timediff(utcnow.as_datetime(begin), utcnow.as_datetime(end))
    assert utcnow.timediff(begin, end) == utcnow.timediff(utcnow.as_datetime(begin), utcnow.get(end))
    assert utcnow.timediff(begin, end) == utcnow.timediff(utcnow.unixtime(begin), utcnow.get(end))
    assert utcnow.timediff(begin, end) == utcnow.timediff(utcnow.unixtime(begin), utcnow.unixtime(end))
    assert utcnow.timediff(begin, end) == utcnow.timediff(begin, utcnow.unixtime(end))


def test_timediff_invalid_unit() -> None:
    import utcnow

    with pytest.raises(ValueError):
        utcnow.timediff(0, 1, "months")
