import json

import pytest


def test_fstring() -> None:
    import utcnow

    result = f"Current server time is {utcnow}"
    assert result.count("-") == 2
    assert result.count(":") == 2
    assert result.count("T") == 1
    assert result.count("Z") == 1
    assert result.endswith("Z")
    assert "Current server time is 2" in result


def test_utcnow_resolution_uniqueness() -> None:
    import utcnow

    result1 = f"Current server time is {utcnow}"
    assert result1.count("-") == 2
    assert result1.count(":") == 2
    assert result1.count("T") == 1
    assert result1.count("Z") == 1
    assert result1.endswith("Z")
    assert "Current server time is 2" in result1

    result2 = f"Current server time is {utcnow.utcnow}"
    assert result2.count("-") == 2
    assert result2.count(":") == 2
    assert result2.count("T") == 1
    assert result2.count("Z") == 1
    assert result2.endswith("Z")
    assert "Current server time is 2" in result2

    result3 = f"Current server time is {utcnow}"
    assert result3.count("-") == 2
    assert result3.count(":") == 2
    assert result3.count("T") == 1
    assert result3.count("Z") == 1
    assert result3.endswith("Z")
    assert "Current server time is 2" in result3

    result4 = f"Current server time is {utcnow.utcnow}"
    assert result4.count("-") == 2
    assert result4.count(":") == 2
    assert result4.count("T") == 1
    assert result4.count("Z") == 1
    assert result4.endswith("Z")
    assert "Current server time is 2" in result4

    assert len(set([result1, result2, result3, result4, "Current server time is " + utcnow.as_string()])) == 5


def test_utcnow_resolution_uniqueness_1000() -> None:
    import utcnow

    assert len(set([str(utcnow) for x in range(1000)]))


def test_uniqueness_as_reference() -> None:
    import utcnow

    dict1 = {"timestamp": str(utcnow)}
    a = str(dict1)
    b = str(dict1)
    assert a == b

    dict2 = {"timestamp": utcnow}
    a = str(dict2)
    b = str(dict2)
    assert a != b


def test_json() -> None:
    import utcnow

    result = json.dumps({"timestamp": str(utcnow)})
    assert utcnow.as_string(json.loads(result).get("timestamp")) == json.loads(result).get("timestamp")

    with pytest.raises(TypeError):
        # 'utcnow' is still an object even if it has a __str__ and __repr__ representation as a timestamp
        json.dumps({"timestamp": utcnow})

    with pytest.raises(TypeError):
        # the same goes for utcnow.utcnow
        json.dumps({"timestamp": utcnow.utcnow})

    # But calling the function will return a string value
    assert len(json.dumps({"timestamp": utcnow.utcnow()})) == 44
    assert len(json.dumps({"timestamp": utcnow()})) == 44  # type: ignore
    assert len(json.dumps({"timestamp": str(utcnow)})) == 44
    assert len(json.dumps({"timestamp": f"{utcnow}"})) == 44
    assert len(json.dumps({"timestamp": f"{utcnow.utcnow}"})) == 44
