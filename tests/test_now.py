import random


def test_now_string() -> None:
    import utcnow

    a = utcnow.get()
    b = utcnow.get()
    c = utcnow.get()
    d = utcnow.get()
    e = utcnow.get()
    f = utcnow.get()
    assert a <= b <= c <= d <= e <= f


def test_now_datetime() -> None:
    import utcnow

    a = utcnow.as_datetime()
    b = utcnow.as_datetime()
    c = utcnow.as_datetime()
    d = utcnow.as_datetime()
    e = utcnow.as_datetime()
    f = utcnow.as_datetime()
    assert a <= b <= c <= d <= e <= f


def test_now_protobuf() -> None:
    import utcnow

    a = utcnow.as_unixtime(utcnow.as_protobuf())
    b = utcnow.as_unixtime(utcnow.as_protobuf())
    c = utcnow.as_unixtime(utcnow.as_protobuf())
    d = utcnow.as_unixtime(utcnow.as_protobuf())
    e = utcnow.as_unixtime(utcnow.as_protobuf())
    f = utcnow.as_unixtime(utcnow.as_protobuf())

    assert a <= b <= c <= d <= e <= f


def test_now_list_string() -> None:
    import utcnow

    list_a = [utcnow.get() for _ in range(10000)]
    list_b = list_a
    list_c = list_a[:]

    assert list_a == list_b
    assert list_a is list_b
    assert list_a == list_c
    assert list_b == list_c
    assert list_a is not list_c
    assert list_b is not list_c

    random.shuffle(list_c)

    assert list_a == list_b
    assert list_a is list_b
    assert list_a != list_c
    assert list_b != list_c
    assert list_a is not list_c
    assert list_b is not list_c

    list_d = sorted(list_c)

    assert list_a == list_b
    assert list_a is list_b
    assert list_a == list_d
    assert list_b == list_d
    assert list_c != list_d
    assert list_a is not list_d
    assert list_b is not list_d
    assert list_c is not list_d


def test_now_list_datetime() -> None:
    import utcnow

    list_a = [utcnow.as_datetime() for _ in range(10000)]
    list_b = list_a
    list_c = list_a[:]

    assert list_a == list_b
    assert list_a is list_b
    assert list_a == list_c
    assert list_b == list_c
    assert list_a is not list_c
    assert list_b is not list_c

    random.shuffle(list_c)

    assert list_a == list_b
    assert list_a is list_b
    assert list_a != list_c
    assert list_b != list_c
    assert list_a is not list_c
    assert list_b is not list_c

    list_d = sorted(list_c)

    assert list_a == list_b
    assert list_a is list_b
    assert list_a == list_d
    assert list_b == list_d
    assert list_c != list_d
    assert list_a is not list_d
    assert list_b is not list_d
    assert list_c is not list_d


def test_utcnow_now_functionality() -> None:
    import utcnow
    from utcnow import now, utcnow_

    assert type(utcnow.now) is not str  # type: ignore
    assert not isinstance(utcnow.now, str)
    assert type(utcnow.utcnow.now) is not str  # type: ignore
    assert not isinstance(utcnow.utcnow.now, str)
    assert type(utcnow_.now) is not str  # type: ignore
    assert not isinstance(utcnow_.now, str)
    assert type(now) is not str  # type: ignore
    assert not isinstance(now, str)

    assert type(utcnow.now()) is str
    assert isinstance(utcnow.now(), str)
    assert type(utcnow.utcnow.now()) is str
    assert isinstance(utcnow.utcnow.now(), str)
    assert type(utcnow_.now()) is str
    assert isinstance(utcnow_.now(), str)
    assert type(now()) is str
    assert isinstance(now(), str)

    assert len(str(utcnow.now)) == 27
    assert len(repr(utcnow.now)) == 27
    assert len(utcnow.now()) == 27
    assert len(str(utcnow.utcnow.now)) == 27
    assert len(repr(utcnow.utcnow.now)) == 27
    assert len(utcnow.utcnow.now()) == 27
    assert len(str(utcnow_.now)) == 27
    assert len(repr(utcnow_.now)) == 27
    assert len(utcnow_.now()) == 27
    assert len(str(now)) == 27
    assert len(repr(now)) == 27
    assert len(now()) == 27

    a = utcnow.now()
    b = utcnow.now()
    c = utcnow.now()
    d = utcnow.now()
    e = utcnow.now()
    f = utcnow.now()
    assert a <= b <= c <= d <= e <= f

    a = str(utcnow.now)
    b = str(utcnow.now)
    c = str(utcnow.now)
    d = str(utcnow.now)
    e = str(utcnow.now)
    f = str(utcnow.now)
    assert a <= b <= c <= d <= e <= f

    a = utcnow.utcnow.now()
    b = utcnow.utcnow.now()
    c = utcnow.utcnow.now()
    d = utcnow.utcnow.now()
    e = utcnow.utcnow.now()
    f = utcnow.utcnow.now()
    assert a <= b <= c <= d <= e <= f

    a = str(utcnow.utcnow.now)
    b = str(utcnow.utcnow.now)
    c = str(utcnow.utcnow.now)
    d = str(utcnow.utcnow.now)
    e = str(utcnow.utcnow.now)
    f = str(utcnow.utcnow.now)
    assert a <= b <= c <= d <= e <= f

    a = utcnow_.now()
    b = utcnow_.now()
    c = utcnow_.now()
    d = utcnow_.now()
    e = utcnow_.now()
    f = utcnow_.now()
    assert a <= b <= c <= d <= e <= f

    a = str(utcnow_.now)
    b = str(utcnow_.now)
    c = str(utcnow_.now)
    d = str(utcnow_.now)
    e = str(utcnow_.now)
    f = str(utcnow_.now)
    assert a <= b <= c <= d <= e <= f

    a = now()
    b = now()
    c = now()
    d = now()
    e = now()
    f = now()
    assert a <= b <= c <= d <= e <= f

    a = str(now)
    b = str(now)
    c = str(now)
    d = str(now)
    e = str(now)
    f = str(now)
    assert a <= b <= c <= d <= e <= f
