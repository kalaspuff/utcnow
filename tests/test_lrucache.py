import datetime
import time
from typing import Callable, Tuple


def hits_miss_currsize(func: Callable) -> Tuple[int, int, int]:
    hits: int = 0
    misses: int = 0
    currsize: int = 0

    hits, misses, _, currsize = func.cache_info()  # type: ignore
    return (hits, misses, currsize)


def test_functional_cache_hits() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    _is_numeric("1")
    assert hits_miss_currsize(_is_numeric) == (0, 1, 1)

    _is_numeric("1")
    assert hits_miss_currsize(_is_numeric) == (1, 1, 1)

    _is_numeric("2")
    assert hits_miss_currsize(_is_numeric) == (1, 2, 2)

    _is_numeric("4711")
    assert hits_miss_currsize(_is_numeric) == (1, 3, 3)

    _is_numeric("4711.0")
    assert hits_miss_currsize(_is_numeric) == (1, 4, 4)

    _is_numeric("4711.00")
    assert hits_miss_currsize(_is_numeric) == (1, 5, 5)

    _is_numeric("4711.00")
    assert hits_miss_currsize(_is_numeric) == (2, 5, 5)

    _is_numeric("4711.")
    assert hits_miss_currsize(_is_numeric) == (2, 6, 6)

    assert hits_miss_currsize(_transform_value) == (0, 0, 0)

    utcnow.get(1)
    assert hits_miss_currsize(_is_numeric) == (2, 6, 6)

    utcnow.get("1")
    assert hits_miss_currsize(_is_numeric) == (3, 6, 6)

    utcnow.get("2")
    assert hits_miss_currsize(_is_numeric) == (4, 6, 6)

    utcnow.get("3")
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get("3")
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get(3)
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get(3.0)
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get(3.0)
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get(3.000)
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get(3.001)
    assert hits_miss_currsize(_is_numeric) == (4, 7, 7)

    utcnow.get("3.")
    assert hits_miss_currsize(_is_numeric) == (4, 8, 8)

    utcnow.get("3.0")
    assert hits_miss_currsize(_is_numeric) == (4, 9, 9)

    assert hits_miss_currsize(_is_numeric) == (4, 9, 9)
    assert hits_miss_currsize(_transform_value) == (3, 9, 9)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.as_datetime(0)
    utcnow.as_datetime(0)
    utcnow.as_datetime("0")
    utcnow.as_datetime(0.0)
    utcnow.as_datetime(-0)
    utcnow.as_datetime(-0.0)
    utcnow.as_datetime("1")
    utcnow.as_datetime("2")
    utcnow.as_datetime("3")
    utcnow.as_datetime("1")
    utcnow.as_datetime("2")
    utcnow.as_datetime("3")
    utcnow.as_datetime("3")
    utcnow.as_datetime("3.")
    utcnow.as_datetime("3")
    utcnow.as_datetime("1.0")
    utcnow.as_datetime("2.0")
    utcnow.as_datetime("3.0")
    utcnow.as_datetime("1.00")
    utcnow.as_datetime("2.00")
    utcnow.as_datetime("3.00")
    utcnow.as_datetime("1.00")
    utcnow.as_datetime("2.00")
    utcnow.as_datetime("3.00")
    utcnow.as_datetime(1.00)
    utcnow.as_datetime(2.00)
    utcnow.as_datetime(3.00)
    utcnow.as_datetime(1.0)
    utcnow.as_datetime(2.0)
    utcnow.as_datetime(3.0)
    utcnow.as_datetime(1.0)
    utcnow.as_datetime(2.0)
    utcnow.as_datetime(3.0)
    utcnow.as_datetime("-0")
    utcnow.as_datetime("-0.")
    utcnow.as_datetime("-0.0")

    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (9, 22, 22)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 19, 19)

    utcnow.get("1970-01-01")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (9, 23, 23)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 19, 19)

    utcnow.get("1970-01-01")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (10, 23, 23)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 19, 19)

    utcnow.get("1970-01-01T00:00:00.000000Z")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (10, 24, 24)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 19, 19)

    utcnow.as_datetime("1970-01-01")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (11, 24, 24)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 20, 20)

    utcnow.as_datetime("1970-01-02")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (11, 25, 25)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 21, 21)

    utcnow.as_datetime("1970-01-01T00:00:00.000000Z")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 25, 25)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 22, 22)

    utcnow.as_datetime("1970-01-01T00:00:00.000000")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 26, 26)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 23, 23)

    utcnow.as_datetime("1970-01-01 00:00:00")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 27, 27)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 24, 24)

    utcnow.as_datetime("1970-01-01 00:00:00+00:00")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 28, 28)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 25, 25)

    utcnow.as_datetime("1970-01-01 00:00:00.000000")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 29, 29)
    assert hits_miss_currsize(_timestamp_to_datetime) == (17, 26, 26)

    utcnow.as_datetime("1970-01-01T00:00:00.000000")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 29, 29)
    assert hits_miss_currsize(_timestamp_to_datetime) == (18, 26, 26)

    utcnow.get("1970-01-01 00:00")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (12, 30, 30)
    assert hits_miss_currsize(_timestamp_to_datetime) == (18, 26, 26)

    utcnow.get("1970-01-01 00:00:00")
    assert hits_miss_currsize(_is_numeric) == (4, 18, 18)
    assert hits_miss_currsize(_transform_value) == (13, 30, 30)
    assert hits_miss_currsize(_timestamp_to_datetime) == (18, 26, 26)


def test_cache_hits_similar() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    values = list(
        map(
            utcnow.get,
            [
                1,
                1,
                1.0,
                1.0,
                1.0,
                1.00,
                1.000,
                "1",
                "1.",
                "1.0",
                "1.00",
                "1.000",
                "1.000",
                "1970-01-01T00:00:01.000000Z",
                "1970-01-01T00:00:01.000000+00:00",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01Z",
                "1970-01-01T00:00:01+00:00",
                "1970-01-01T00:00:01",
                "1970-01-01T00:00:01.0Z",
                "1970-01-01T00:00:01.0+00:00",
                "1970-01-01T00:00:01.000+00:00",
                "1970-01-01T00:00:01.000",
            ],
        )
    )

    assert len(list(filter(lambda value: value == "1970-01-01T00:00:01.000000Z", values))) == 24

    assert hits_miss_currsize(_is_numeric) == (0, 5, 5)
    assert hits_miss_currsize(_transform_value) == (7, 17, 17)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    values2 = list(
        map(
            utcnow.get,
            [
                1,
                1,
                1.0,
                1.0,
                1.0,
                1.00,
                1.000,
                "1",
                "1.",
                "1.0",
                "1.00",
                "1.000",
                "1.000",
                "1970-01-01T00:00:01.000000Z",
                "1970-01-01T00:00:01.000000+00:00",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01Z",
                "1970-01-01T00:00:01+00:00",
                "1970-01-01T00:00:01",
                "1970-01-01T00:00:01.0Z",
                "1970-01-01T00:00:01.0+00:00",
                "1970-01-01T00:00:01.000+00:00",
                "1970-01-01T00:00:01.000",
            ],
        )
    )

    assert len(list(filter(lambda value: value == "1970-01-01T00:00:01.000000Z", values2))) == 24

    assert hits_miss_currsize(_is_numeric) == (0, 5, 5)
    assert hits_miss_currsize(_transform_value) == (7 + 24, 17, 17)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    values3 = list(
        map(
            utcnow.as_datetime,
            [
                1,
                1,
                1.0,
                1.0,
                1.0,
                1.00,
                1.000,
                "1",
                "1.",
                "1.0",
                "1.00",
                "1.000",
                "1.000",
                "1970-01-01T00:00:01.000000Z",
                "1970-01-01T00:00:01.000000+00:00",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01.000000",
                "1970-01-01T00:00:01Z",
                "1970-01-01T00:00:01+00:00",
                "1970-01-01T00:00:01",
                "1970-01-01T00:00:01.0Z",
                "1970-01-01T00:00:01.0+00:00",
                "1970-01-01T00:00:01.000+00:00",
                "1970-01-01T00:00:01.000",
            ],
        )
    )

    assert (
        len(
            list(
                filter(
                    lambda value: value == datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc), values3
                )
            )
        )
        == 24
    )

    assert hits_miss_currsize(_is_numeric) == (0, 5, 5)
    assert hits_miss_currsize(_transform_value) == (48, 17, 17)
    assert hits_miss_currsize(_timestamp_to_datetime) == (7, 17, 17)

    values4 = list(map(utcnow.get, values3))

    assert len(list(filter(lambda value: value == "1970-01-01T00:00:01.000000Z", values4))) == 24

    assert hits_miss_currsize(_is_numeric) == (0, 5, 5)
    assert hits_miss_currsize(_transform_value) == (71, 18, 18)
    assert hits_miss_currsize(_timestamp_to_datetime) == (7, 17, 17)


def test_cache_hits_with_sentinel() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.get()

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.as_datetime()

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.utcnow()

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow()  # type: ignore

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)


def test_cache_hits_with_sentinel_loop() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    call_count = 100
    values = set()

    for _ in range(call_count):
        values.add(utcnow.get())
        time.sleep(0.00001)

    assert len(values) == call_count
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(utcnow())  # type: ignore
        time.sleep(0.00001)

    assert len(values) == call_count * 2
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(f"{utcnow}")
        time.sleep(0.00001)

    assert len(values) == call_count * 3
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(f"{utcnow.utcnow}")
        time.sleep(0.00001)

    assert len(values) == call_count * 4
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow()))  # type: ignore
        time.sleep(0.00001)

    assert len(values) == call_count * 5
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow))
        time.sleep(0.00001)

    assert len(values) == call_count * 6
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow.utcnow))
        time.sleep(0.00001)

    assert len(values) == call_count * 7
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow.utcnow()))
        time.sleep(0.00001)

    assert len(values) == call_count * 8
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow.as_string()))
        time.sleep(0.00001)

    assert len(values) == call_count * 9
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(str(utcnow.as_datetime()))
        time.sleep(0.00001)

    assert len(values) == call_count * 10
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    d = {"timestamp": str(utcnow)}
    for _ in range(call_count):
        values.add(str(d))
        time.sleep(0.00001)

    assert len(values) == call_count * 10 + 1
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    d = {"timestamp": str(utcnow)}
    for _ in range(call_count):
        values.add(str(d))
        time.sleep(0.00001)

    assert len(values) == call_count * 10 + 2
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    d = {"timestamp": utcnow}  # type: ignore
    for _ in range(call_count):
        values.add(str(d))
        time.sleep(0.00001)

    assert len(values) == call_count * 11 + 2
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    d = {"timestamp": utcnow.utcnow}  # type: ignore
    for _ in range(call_count):
        values.add(str(d))
        time.sleep(0.00001)

    assert len(values) == call_count * 12 + 2
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)


def test_cache_hits_with_uniques() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.get(time.time())
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 1, 1)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    utcnow.as_datetime(time.time())
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 2, 2)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 1, 1)

    utcnow.utcnow(time.time())
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 3, 3)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 1, 1)

    utcnow(time.time())  # type: ignore
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 4, 4)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 1, 1)

    utcnow.get(0)
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 5, 5)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 1, 1)

    utcnow.as_datetime(0)
    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (1, 5, 5)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 2, 2)

    utcnow.get("0")
    assert hits_miss_currsize(_is_numeric) == (0, 1, 1)
    assert hits_miss_currsize(_transform_value) == (1, 6, 6)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 2, 2)

    utcnow.as_datetime("0")
    assert hits_miss_currsize(_is_numeric) == (0, 1, 1)
    assert hits_miss_currsize(_transform_value) == (2, 6, 6)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 3, 3)

    utcnow.get(str(time.time()))
    assert hits_miss_currsize(_is_numeric) == (0, 2, 2)
    assert hits_miss_currsize(_transform_value) == (2, 7, 7)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 3, 3)

    utcnow.as_datetime(str(time.time()))
    assert hits_miss_currsize(_is_numeric) == (0, 3, 3)
    assert hits_miss_currsize(_transform_value) == (2, 8, 8)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 4, 4)

    t = time.time()

    utcnow.get(t)
    assert hits_miss_currsize(_is_numeric) == (0, 3, 3)
    assert hits_miss_currsize(_transform_value) == (2, 9, 9)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 4, 4)

    utcnow.as_datetime(t)
    assert hits_miss_currsize(_is_numeric) == (0, 3, 3)
    assert hits_miss_currsize(_transform_value) == (3, 9, 9)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 5, 5)

    utcnow.get(str(t))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (3, 10, 10)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 5, 5)

    utcnow.as_datetime(str(t))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 10, 10)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 6, 6)

    utcnow.as_datetime(str(t))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 10, 10)
    assert hits_miss_currsize(_timestamp_to_datetime) == (1, 6, 6)

    utcnow.as_datetime(t)
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 10, 10)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 6, 6)

    utcnow.get("2020-02-29T03:01:13.000020-00:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 11, 11)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 6, 6)

    utcnow.get("2020-02-29T03:01:13.000020+00:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 12, 12)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 6, 6)

    utcnow.get("2020-02-29T04:01:13.000020+01:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 13, 13)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 6, 6)

    utcnow.as_datetime("2020-02-29T05:01:13.00002+02:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 14, 14)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 7, 7)

    utcnow.as_datetime("2020-02-29T06:01:13.000020+03:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 15, 15)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 8, 8)

    utcnow.as_datetime("2020-02-29 03:01:13.000020Z")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 16, 16)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 9, 9)

    utcnow.as_datetime(datetime.datetime(2020, 2, 29, 3, 1, 13, 20))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 17, 17)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 10, 10)

    utcnow.as_datetime(datetime.datetime(2020, 2, 29, 3, 1, 13, 20, tzinfo=datetime.timezone.utc))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 18, 18)
    assert hits_miss_currsize(_timestamp_to_datetime) == (2, 11, 11)

    utcnow.as_datetime(datetime.datetime(2020, 2, 29, 3, 1, 13, 20, tzinfo=datetime.timezone.utc))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 18, 18)
    assert hits_miss_currsize(_timestamp_to_datetime) == (3, 11, 11)

    utcnow.as_datetime(datetime.datetime(2020, 2, 29, 3, 1, 13, 21, tzinfo=datetime.timezone.utc))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 19, 19)
    assert hits_miss_currsize(_timestamp_to_datetime) == (3, 12, 12)

    tz = datetime.timezone(offset=datetime.timedelta(hours=-4))
    utcnow.as_datetime(datetime.datetime(2020, 2, 28, 23, 1, 13, 21, tzinfo=tz))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 19, 19)
    assert hits_miss_currsize(_timestamp_to_datetime) == (4, 12, 12)

    utcnow.as_datetime("2020-02-29 00:00")
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (4, 20, 20)
    assert hits_miss_currsize(_timestamp_to_datetime) == (4, 13, 13)

    utcnow.as_datetime(utcnow.get("2020-02-29 00:00"))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (5, 21, 21)
    assert hits_miss_currsize(_timestamp_to_datetime) == (4, 14, 14)

    tz = datetime.timezone(offset=datetime.timedelta(hours=-1))
    utcnow.as_datetime(datetime.datetime(2020, 2, 28, 23, 0, tzinfo=tz))
    assert hits_miss_currsize(_is_numeric) == (0, 4, 4)
    assert hits_miss_currsize(_transform_value) == (5, 22, 22)
    assert hits_miss_currsize(_timestamp_to_datetime) == (4, 15, 15)


def test_cache_hits_with_uniques_loop() -> None:
    import utcnow
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, 0, 0)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    call_count = 100
    values = set()

    for _ in range(call_count):
        values.add(utcnow.get(time.time()))
        time.sleep(0.00001)

    assert len(values) == call_count

    assert hits_miss_currsize(_is_numeric) == (0, 0, 0)
    assert hits_miss_currsize(_transform_value) == (0, call_count, call_count)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(utcnow.get(str(time.time())))
        time.sleep(0.00001)

    assert len(values) == call_count * 2

    assert hits_miss_currsize(_is_numeric) == (0, call_count, call_count)
    assert hits_miss_currsize(_transform_value) == (0, call_count * 2, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    t = time.time()
    for _ in range(call_count):
        values.add(utcnow.get(t))
        time.sleep(0.00001)

    assert len(values) == call_count * 2 + 1

    assert hits_miss_currsize(_is_numeric) == (0, call_count, call_count)
    assert hits_miss_currsize(_transform_value) == (call_count - 1, call_count * 2 + 1, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    t_str = str(time.time())
    for _ in range(call_count):
        values.add(utcnow.get(t_str))
        time.sleep(0.00001)

    assert len(values) == call_count * 2 + 2

    assert hits_miss_currsize(_is_numeric) == (0, call_count + 1, call_count + 1)
    assert hits_miss_currsize(_transform_value) == ((call_count - 1) * 2, call_count * 2 + 2, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    t_dt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    for _ in range(call_count):
        values.add(utcnow.get(t_dt))
        time.sleep(0.00001)

    assert len(values) == call_count * 2 + 3

    assert hits_miss_currsize(_is_numeric) == (0, call_count + 1, call_count + 1)
    assert hits_miss_currsize(_transform_value) == ((call_count - 1) * 3, call_count * 2 + 3, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    t_dt = datetime.datetime.now(datetime.timezone.utc)
    for _ in range(call_count):
        values.add(utcnow.get(t_dt))
        time.sleep(0.00001)

    assert len(values) == call_count * 2 + 4

    assert hits_miss_currsize(_is_numeric) == (0, call_count + 1, call_count + 1)
    assert hits_miss_currsize(_transform_value) == ((call_count - 1) * 4, call_count * 2 + 4, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)

    for _ in range(call_count):
        values.add(utcnow.get(datetime.datetime.now(datetime.timezone.utc)))
        time.sleep(0.00001)

    assert len(values) == call_count * 3 + 4

    assert hits_miss_currsize(_is_numeric) == (0, call_count + 1, call_count + 1)
    assert hits_miss_currsize(_transform_value) == ((call_count - 1) * 4, call_count * 3 + 4, 128)
    assert hits_miss_currsize(_timestamp_to_datetime) == (0, 0, 0)
