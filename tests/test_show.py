from dataclasses import dataclass
from uiwiz import ui
from bs4 import BeautifulSoup


def test_show_dict():
    dic = {"a": 1, "b": 2}
    output = str(ui.show(dic))
    assert output is not None


def test_show_dict_values():
    dic = {"a": 1, "b": 2}
    output = str(ui.show(dic))
    soup = BeautifulSoup(output)
    assert soup.select("#a-4")[0].next == "1"
    assert soup.select("#a-7")[0].next == "2"


@dataclass
class Data:
    a: int
    b: int


def test_show_dataclass():
    data = Data(1, 2)
    output = str(ui.show(data))
    assert output is not None


def test_show_dataclass_values():
    data = Data(1, 2)
    output = str(ui.show(data))
    soup = BeautifulSoup(output)
    assert soup.select("#a-4")[0].next == "1"
    assert soup.select("#a-7")[0].next == "2"


def test_show_list():
    lst = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    output = str(ui.show(lst))
    assert output is not None


def test_show_list_values():
    lst = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    output = str(ui.show(lst))
    soup = BeautifulSoup(output)
    assert soup.select("#a-8")[0].next == "1"
    assert soup.select("#a-9")[0].next == "2"
    assert soup.select("#a-11")[0].next == "3"
    assert soup.select("#a-12")[0].next == "4"
