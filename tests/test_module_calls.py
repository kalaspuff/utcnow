import datetime


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