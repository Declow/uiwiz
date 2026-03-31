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


def test_dict_duplicate_values_keep_separator_for_non_last_items() -> None:
    output = str(ui.dict({"a": 1, "b": 1}))
    assert "&quot;a&quot;:" in output
    assert "&quot;b&quot;:" in output
    assert output.count(",</div>") >= 1


def test_dict_list_duplicate_values_keep_separator_for_non_last_items() -> None:
    output = str(ui.dict([1, 1]))
    assert output.count(",</div>") >= 1
