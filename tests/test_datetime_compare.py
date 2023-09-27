import random


def test_sorted_timestamp_list() -> None:
    import utcnow

    values = [
        "2021-02-28T10:10:58.123980Z",
        "2021-02-28T10:10:59.123980Z",
        "2021-02-18-01:00",
        "2021-01-02T00:00:00.04000Z",
        "1984-08-01T13:38:00.004711Z",
        "2021-01-02T00:00:00.04-00:00",
        "2021-01-02T00:00:00.05000+00:00",
        "2021-01-01T00:59:59.999998+02:00",
        "2021-01-02T00:01:00.045-01:00",
        "2021-01-02T00:01:00Z",
        "1990-12-31T15:59:59-08:00",
        "2021-01-02T00:00:00.049996-00:00",
        "1985-04-12T23:20:50.520001+00:00",
        "2020-02-18T23:55:10",
        "2021-02-28 10:10:59.12398 UTC",
        "2021-01-02T00:00:00.04001",
        "2021-01-02T00:00:00.04000+00:00",
        "2021-01-01T00:59:59.999998Z",
        "2021-01-02T00:00:00.049997-01:00",
        "2021-01-01 00:00:00.1",
        "2020-02-18T23:55",
        "2020-02-18T23:55:10.0",
        "2020-02-18T23:55:10.0-05:00",
        "2021-01-01 00:00:00",
        "2021-02-18 01:00",
        "1937-01-01T12:00:27.87+00:20",
        "1985-04-12T23:20:50.5",
        "2021-02-28 10:10:59.123980Z",
        "2021-02-18 03:00+01:00",
        "2021-01-02T00:00:00.06-01:00",
        "2020-02-18 23:55:10.550+05:00",
        "2020-02-18 23:55:10.550-01:00",
        "2021-01-02T00:01:00.045-02:00",
        "2021-01-02T00:00:00.03",
        "1985-04-12T23:20:50.52Z",
        "2021-01-02T00:00:00.049999",
        "2021-01-02T00:01:00.045+01:00",
        "2021-02-28 10:10:59.123979+00:00",
        "2021-01-02T00:00:00.049998+01:00",
        "2021-02-18+01:00",
        "1996-12-19T16:39:57-08:00",
        "2021-01-01T00:59:59.999998-02:00",
        "2021-01-02T00:01:00.045+02:00",
        "2021-01-02T00:00:00.04000 UTC",
        "2021-01-02T00:00:00.05+00:00",
        "1984-08-01",
        "2021-01-01T23:59:59.999998Z",
        "2021-01-01T23:59:59.999999Z",
        "2021-01-01T00:00:00.02",
        "2020-02-18T23:55:10.0+05:00",
        "2021-02-18",
        "2020-02-18T23:55:10.550-05:00",
    ]

    list_alphabetical_order = sorted(values)
    list_alphabetical_order_reversed = sorted(values, reverse=True)

    assert list_alphabetical_order != values
    assert list_alphabetical_order_reversed != values
    assert list_alphabetical_order != list_alphabetical_order_reversed

    list_datetime_order = sorted(values, key=utcnow.as_datetime)
    list_rfc3799_timestamp_order = sorted(values, key=utcnow.rfc3339_timestamp)

    assert list_datetime_order == list_rfc3799_timestamp_order

    assert sorted(list_alphabetical_order_reversed, key=utcnow.as_datetime) != list_datetime_order
    assert sorted(list_alphabetical_order_reversed, key=utcnow.rfc3339_timestamp) != list_rfc3799_timestamp_order

    assert sorted(list_alphabetical_order_reversed) == sorted(list_alphabetical_order)
    assert sorted(list_alphabetical_order_reversed, key=utcnow.as_datetime) != sorted(
        list_alphabetical_order, key=utcnow.as_datetime
    )
    assert sorted(list_alphabetical_order_reversed, key=utcnow.rfc3339_timestamp) != sorted(
        list_alphabetical_order, key=utcnow.rfc3339_timestamp
    )

    assert sorted(sorted(list_alphabetical_order_reversed), key=utcnow.as_datetime) == sorted(
        sorted(list_alphabetical_order), key=utcnow.as_datetime
    )
    assert sorted(sorted(list_alphabetical_order_reversed), key=utcnow.rfc3339_timestamp) == sorted(
        sorted(list_alphabetical_order), key=utcnow.rfc3339_timestamp
    )

    list_output_datetimes_reordered = list(
        map(utcnow.as_datetime, sorted(list_alphabetical_order_reversed, key=utcnow.as_datetime))
    )
    list_output_datetimes_ordered = list(
        map(utcnow.as_datetime, sorted(list_alphabetical_order, key=utcnow.as_datetime))
    )
    list_output_strings_reordered = list(
        map(utcnow.rfc3339_timestamp, sorted(list_alphabetical_order_reversed, key=utcnow.rfc3339_timestamp))
    )
    list_output_strings_ordered = list(
        map(utcnow.rfc3339_timestamp, sorted(list_alphabetical_order, key=utcnow.rfc3339_timestamp))
    )

    assert list_output_datetimes_reordered == list_output_datetimes_ordered
    assert list_output_strings_reordered == list_output_strings_ordered

    assert sorted(map(utcnow.as_datetime, values)) == list_output_datetimes_reordered == list_output_datetimes_ordered
    assert (
        sorted(map(utcnow.rfc3339_timestamp, values)) == list_output_strings_reordered == list_output_strings_reordered
    )

    expected_list = sorted(map(utcnow.rfc3339_timestamp, values))

    for _ in range(0, 20):
        shuffled_values = values[:]
        random.shuffle(shuffled_values)

        assert sorted(map(utcnow.rfc3339_timestamp, shuffled_values)) == expected_list
        assert sorted(map(utcnow.as_datetime, shuffled_values)) == list(map(utcnow.as_datetime, expected_list))
        assert sorted(map(utcnow.unixtime, shuffled_values)) == list(map(utcnow.unixtime, expected_list))

        assert (
            list(map(utcnow.rfc3339_timestamp, sorted(shuffled_values, key=utcnow.rfc3339_timestamp))) == expected_list
        )
        assert list(map(utcnow.rfc3339_timestamp, sorted(shuffled_values, key=utcnow.as_datetime))) == expected_list
        assert list(map(utcnow.rfc3339_timestamp, sorted(shuffled_values, key=utcnow.unixtime))) == expected_list
