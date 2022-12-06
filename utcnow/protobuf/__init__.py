import sys
from typing import Any

try:
    from google.protobuf.message import Message as GenericProtobufMessage  # noqa
except Exception:  # pragma: no cover

    class _GenericProtobufMessage(object):
        pass

    this_module = sys.modules[__name__]
    setattr(this_module, "GenericProtobufMessage", _GenericProtobufMessage)

try:
    from google.protobuf.timestamp_pb2 import Timestamp  # noqa

    TimestampProtobufMessage = Timestamp
except Exception:  # pragma: no cover

    class _TimestampProtobufMessage(object):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise Exception("google.protobuf package not installed")

        def SerializeToString(self, *args: Any, **kwargs: Any) -> None:
            raise Exception("google.protobuf package not installed")

        def FromString(self, *args: Any, **kwargs: Any) -> None:
            raise Exception("google.protobuf package not installed")

        def ParseFromString(self, *args: Any, **kwargs: Any) -> None:
            raise Exception("google.protobuf package not installed")

        def MergeFromString(self, *args: Any, **kwargs: Any) -> None:
            raise Exception("google.protobuf package not installed")

    this_module = sys.modules[__name__]
    setattr(this_module, "Timestamp", _TimestampProtobufMessage)
    setattr(this_module, "TimestampProtobufMessage", _TimestampProtobufMessage)


__all__ = [
    "GenericProtobufMessage",
    "Timestamp",
    "TimestampProtobufMessage",
]
