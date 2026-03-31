from uiwiz import ui


def test_toggle():
    output = str(ui.toggle("name", checked=False))
    assert output == '<input id="a-0" class="toggle toggle-md" type="checkbox" name="name">'


def test_toggle_checked():
    output = str(ui.toggle("name", checked=True))
    assert output == '<input id="a-0" class="toggle toggle-md" checked="checked" type="checkbox" name="name">'
