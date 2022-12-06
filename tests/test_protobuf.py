import datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp


def protobuf_timestamp_from_json_string(json_string: str) -> Timestamp:
    """Convert a JSON string (RFC3339) to a protobuf Timestamp."""
    message = Timestamp()
    message.FromJsonString(json_string)
    return message


@pytest.mark.parametrize(
    "value, expected_output, expect_error",
    [
        (Timestamp(), "1970-01-01T00:00:00.000000Z", False),
        (Timestamp(nanos=1000), "1970-01-01T00:00:00.000001Z", False),
        (Timestamp(nanos=1000), "1970-01-01T00:00:00.000001Z", False),
        (Timestamp(nanos=10000000), "1970-01-01T00:00:00.010000Z", False),
        (Timestamp(seconds=1), "1970-01-01T00:00:01.000000Z", False),
        (Timestamp(seconds=1338), "1970-01-01T00:22:18.000000Z", False),
        (Timestamp(seconds=14792, nanos=540000000), "1970-01-01T04:06:32.540000Z", False),
        (Timestamp(nanos=109000), "1970-01-01T00:00:00.000109Z", False),
        (Timestamp(seconds=1614300199, nanos=462145000), "2021-02-26T00:43:19.462145Z", False),
        (Timestamp(seconds=1614300199), "2021-02-26T00:43:19.000000Z", False),
        (Timestamp(nanos=991900000), "1970-01-01T00:00:00.991900Z", False),
        (Timestamp(seconds=-1), "1969-12-31T23:59:59.000000Z", False),
        (Timestamp(nanos=-109000), "1969-12-31T23:59:59.999891Z", False),
        (Timestamp(seconds=-1614300199, nanos=-462145000), "1918-11-05T23:16:40.537855Z", False),
        (Timestamp(seconds=-1614300199), "1918-11-05T23:16:41.000000Z", False),
        (Timestamp(nanos=-991900000), "1969-12-31T23:59:59.008100Z", False),
    ],
)
def test_protobuf_values(value: Timestamp, expected_output: str, expect_error: bool) -> None:
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
        return

    assert utcnow.as_string(value) == expected_output
    assert utcnow.as_string(expected_output) == expected_output
    assert utcnow.as_string(expected_output) == utcnow.as_string(expected_output)
    assert utcnow.as_datetime(value) == utcnow.as_datetime(expected_output)
    assert utcnow.utcnow(utcnow.as_datetime(value)) == utcnow.utcnow(utcnow.as_datetime(expected_output))
    assert utcnow.utcnow(utcnow.as_datetime(value).replace(tzinfo=None)) == expected_output
    assert utcnow.as_string(utcnow.utcnow(utcnow.as_datetime(value))) == expected_output
    assert utcnow.as_string(utcnow.as_protobuf(value).SerializeToString()) == expected_output

    value2 = utcnow.as_protobuf(value)
    assert round(value2.seconds + value2.nanos * 1e-9, 9) == round(value.seconds + value.nanos * 1e-9, 9)

    message = Timestamp()
    message.FromJsonString(utcnow.as_string(value))
    assert round(message.seconds + message.nanos * 1e-9, 9) == round(value.seconds + value.nanos * 1e-9, 9)
    assert utcnow.as_string(message) == expected_output
    assert message == utcnow.as_protobuf(value)


def test_from_protobuf_binary() -> None:
    import utcnow

    protobuf_msg_binary = b"\x08\xc4\xec\xbc\x9c\x06\x10\xa0\xa1\xb0Q"
    assert utcnow.get(protobuf_msg_binary) == "2022-12-06T12:32:04.170660Z"
