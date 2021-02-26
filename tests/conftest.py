import pytest


@pytest.fixture(autouse=True)
def clear_lru_cache() -> None:
    from utcnow import _is_numeric, _timestamp_to_datetime, _transform_value

    _is_numeric.cache_clear()
    _transform_value.cache_clear()
    _timestamp_to_datetime.cache_clear()
