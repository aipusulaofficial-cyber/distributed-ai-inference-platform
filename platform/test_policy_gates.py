from runtime_policy import validate


def test_runtime_bounds():
    assert validate(10, 1)
    assert not validate(31, 1)
    assert not validate(10, 3)
