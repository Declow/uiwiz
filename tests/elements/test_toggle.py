from uiwiz import ui


def test_toggle():
    output = str(ui.toggle("name", False))
    assert '<input id="a-0" class="toggle toggle-md" type="checkbox" name="name">' == output


def test_toggle_checked():
    output = str(ui.toggle("name", True))
    assert '<input id="a-0" class="toggle toggle-md" checked="checked" type="checkbox" name="name">' == output
