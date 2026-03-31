from uiwiz import ui


def test_checkbox():
    output = str(ui.checkbox("name", checked=False))
    assert output == '<input id="a-0" class="checkbox checkbox-md" name="name" type="checkbox">'


def test_checkbox_checked():
    output = str(ui.checkbox("name", checked=True))
    assert output == '<input id="a-0" class="checkbox checkbox-md" checked="checked" name="name" type="checkbox">'
