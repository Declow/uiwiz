from uiwiz import ui


def test_toggle():
    output = str(ui.toggle("name", False))
    assert '<input id="a-0" type="checkbox" name="name" class="toggle ">' == output


def test_toggle_checked():
    output = str(ui.toggle("name", True))
    assert '<input id="a-0" checked="checked" type="checkbox" name="name" class="toggle ">' == output
