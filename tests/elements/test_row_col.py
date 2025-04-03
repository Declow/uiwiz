from uiwiz.elements.col import Col
from uiwiz.elements.row import Row


def test_col_classes():
    col = Col()
    assert col.__root_class__ == "flex flex-col items-start gap-4 p-4 "
    assert col.get_classes() == "flex flex-col items-start gap-4 p-4 "


def test_row_classes():
    row = Row()
    assert row.__root_class__ == "flex flex-row flex-wrap items-start gap-4 "
    assert row.get_classes() == "flex flex-row flex-wrap items-start gap-4 "


def test_row_classes_v2():
    row = Row(padding="p-2")
    assert row.__root_class__ == "flex flex-row flex-wrap items-start gap-4 p-2"
    assert row.get_classes() == "flex flex-row flex-wrap items-start gap-4 p-2"
