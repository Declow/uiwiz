from uiwiz import ui


def test_checkbox():
    output = str(ui.checkbox("name", False))
    assert '<input id="a-0" name="name" type="checkbox" class="checkbox ">' == output


def test_checkbox_checked():
    output = str(ui.checkbox("name", True))
    assert '<input id="a-0" checked="checked" name="name" type="checkbox" class="checkbox ">' == output
