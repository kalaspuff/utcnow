import datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

import utcnow


@pytest.mark.parametrize(
    "value, expect_error",
    [
        ("1970-01-01", False),
        ("2020-01-01", False),
        ("2020-01-29", False),
        ("2020-01-30", False),
        ("2020-01-31", False),
        ("2020-01-32", True),
        ("2020-01-40", True),
        ("2020-01-50", True),
        ("2020-00-00", True),
        ("2020-01-00", True),
        ("2020-00-01", True),
        ("2020-12-01", False),
        ("2020-12-31", False),
        ("2020-12-32", True),
        ("2020-13-01", True),
        ("2020-02-01", False),
        ("2020-02-28", False),
        ("2020-02-29", False),
        ("2020-02-30", True),
        ("2020-02-31", True),
        ("2021-02-28", False),
        ("2021-02-29", True),
    ],
)
def test_dates(value: str, expect_error: bool) -> None:
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

    try:
        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000Z"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000Z"), datetime.datetime)
        if expect_error:
            assert False
    except Exception:
        if not expect_error:
            raise
        if not expect_error:
            # unreachable
            assert False

        assert True

    try:
        assert isinstance(utcnow.as_string(value), str)
        assert isinstance(utcnow.as_datetime(value), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000Z"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000Z"), datetime.datetime)

        assert utcnow.as_string(value) == utcnow.as_string(f"{value}T00:00:00.000000Z")

        assert isinstance(utcnow.as_string(f"{value} 00:00:00.000000Z"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00.000000Z"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value} 00:00:00.000000"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00.000000"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000+00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000+00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value} 00:00:00.000000+00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00.000000+00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000-00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000-00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00.000000 UTC"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00.000000 UTC"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00Z"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00Z"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value} 00:00:00Z"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00Z"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value} 00:00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00+00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00+00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value} 00:00:00+00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value} 00:00:00+00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00-00:00"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00-00:00"), datetime.datetime)

        assert isinstance(utcnow.as_string(f"{value}T00:00:00 UTC"), str)
        assert isinstance(utcnow.as_datetime(f"{value}T00:00:00 UTC"), datetime.datetime)

        if expect_error:
            assert False
    except Exception:
        if not expect_error:
            raise
        if not expect_error:
            # unreachable
            assert False

        assert True


def test_as_date_string() -> None:
    date_today_0 = datetime.datetime.utcnow().date().isoformat()
    assert utcnow.get_today() == date_today_0 or utcnow.get_today() == datetime.datetime.utcnow().date().isoformat()

    assert utcnow.as_date_string("2022-04-04") == "2022-04-04"
    assert utcnow.as_date_string("2021-01-02T00:00:00.04000Z") == "2021-01-02"

    assert utcnow.get_today(tz="+24:00") != utcnow.get_today()
    assert utcnow.get_today(tz="-24:00") != utcnow.get_today()

    assert (
        utcnow.get_today(tz="UTC") == date_today_0
        or utcnow.get_today(tz="UTC") == datetime.datetime.utcnow().date().isoformat()
    )
    assert (
        utcnow.get_today(tz=datetime.timezone.utc) == date_today_0
        or utcnow.get_today(tz=datetime.timezone.utc) == datetime.datetime.utcnow().date().isoformat()
    )

    assert utcnow.get_today(tz=datetime.timezone(datetime.timedelta(hours=24, microseconds=-1))) != utcnow.get_today()
    assert utcnow.get_today(tz=datetime.timezone(datetime.timedelta(hours=24, microseconds=-1))) == utcnow.get_today(
        tz="+24:00"
    ) or utcnow.get_today(tz=datetime.timezone(datetime.timedelta(hours=24, microseconds=-1))) == utcnow.get_today(
        tz="+24:00"
    )

    with pytest.raises(ValueError):
        utcnow.get_today(tz="UnknownTimezone")

    with pytest.raises(ValueError):
        utcnow.get_today(tz=datetime.timezone)  # type:ignore

    with pytest.raises(ValueError):
        utcnow.get_today(tz="+32:00")

    with pytest.raises(ValueError):
        utcnow.get_today(tz="-32:00")

    with pytest.raises(ValueError):
        utcnow.get_today(tz="+TEST")
