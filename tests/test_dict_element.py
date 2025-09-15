import pytest

from uiwiz import ui


def test_dict():
    dic = {"a": 1, "b": 2}
    output = str(ui.dict(dic))
    assert output is not None


def test_dict_exception():
    with pytest.raises(ValueError):
        ui.dict(None)


class Test:
    asd: int


def test_dict_exception_wrong_type():
    with pytest.raises(ValueError):
        ui.dict(Test())
