import datetime


def test_readme_example_skynet() -> None:
    from utcnow import utcnow

    tz_EDT = datetime.timezone(offset=datetime.timedelta(hours=-4))
    dt = datetime.datetime(1997, 8, 4, 2, 14, tzinfo=tz_EDT)
    result = utcnow.as_string(dt)
    expected_str = "1997-08-04T06:14:00.000000Z"
    expected_dt_str = dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    assert result == expected_str
    assert result == expected_dt_str
    assert result == utcnow(result)
    assert result == utcnow(dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
    assert result == utcnow(dt.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
    assert result == utcnow(dt.isoformat())


def test_readme_example_birthday() -> None:
    from utcnow import utcnow

    result = utcnow.as_datetime("1984-08-01T13:38:00.123450Z")
    expected_dt = datetime.datetime(1984, 8, 1, 13, 38, 0, 123450, tzinfo=datetime.timezone.utc)
    assert result == expected_dt


def test_readme_simple_transform() -> None:
    from utcnow import utcnow

    dt = datetime.datetime(1984, 8, 1, 13, 38, 0, 4711)
    result = utcnow.as_string(dt)
    expected_str = "1984-08-01T13:38:00.004711Z"

    assert result == expected_str
    assert result == utcnow(dt)
    assert result == dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert result == dt.isoformat() + "Z"
    assert result == utcnow(result)
    assert result == utcnow(dt.isoformat())
    assert result == utcnow(dt.isoformat() + "+00:00")
    assert result == utcnow(dt.isoformat() + "-00:00")
    assert result == utcnow(dt.isoformat() + " UTC")
    assert result == utcnow(dt.replace(tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
    assert result == utcnow(dt.replace(tzinfo=datetime.timezone.utc).isoformat())


def test_readme_datetime_complement() -> None:
    import utcnow

    dt = datetime.datetime.utcnow()
    expected_str = dt.isoformat() + "Z"

    assert len(expected_str) == 27

    assert expected_str[0] == "2"
    assert expected_str[-1] == "Z"
    assert expected_str.count("-") == 2
    assert expected_str.count(":") == 2
    assert expected_str.count("T") == 1
    assert expected_str.count("Z") == 1

    assert expected_str == utcnow.utcnow(dt)
    assert expected_str == utcnow.utcnow(dt)
    assert expected_str == utcnow(dt)  # type: ignore
    assert expected_str == utcnow(dt)  # type: ignore
    assert expected_str == utcnow.as_string(dt)
    assert expected_str == utcnow.utcnow.as_string(dt)
    assert expected_str == utcnow.as_datetime(dt).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert expected_str == utcnow.as_datetime(dt).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert expected_str == utcnow.as_datetime(dt).replace(tzinfo=None).isoformat() + "Z"

    assert expected_str != utcnow.as_datetime(dt).isoformat() + "Z"
    assert expected_str != dt.replace(tzinfo=datetime.timezone.utc).isoformat() + "Z"
    assert expected_str != dt.astimezone(datetime.timezone.utc).isoformat() + "Z"
    assert expected_str != dt.astimezone(datetime.timezone.utc).isoformat()
    assert expected_str != dt.replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    assert expected_str != dt.replace(tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    assert expected_str != dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    # '2021-02-18T08:24:48.382262Z'
    # same thing can be accomplished using datetime and all of these calls returns the same str value:
    # 1. utcnow.utcnow()
    # 2. str(utcnow)
    # 3. str(utcnow.utcnow)
    # 4. utcnow.as_string()
    # 5. utcnow.utcnow.as_string()
    # 6. datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    # 7. datetime.datetime.utcnow().isoformat() + "Z"
    # 8. datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
