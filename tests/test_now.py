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
