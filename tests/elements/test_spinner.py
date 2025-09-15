from uiwiz import ui


def test_spinner():
    spin = None
    with ui.button("Click me") as btn:
        spin = ui.spinner(btn)
    assert f"#{spin.id}" == btn.attributes["hx-indicator"]


def test_spinner_multiple():
    spin = None
    tx = ui.textarea("Hello")
    with ui.button("Click me") as btn:
        spin = ui.spinner(btn, tx)
    assert f"#{spin.id}" == btn.attributes["hx-indicator"]
    assert f"#{spin.id}" == tx.attributes["hx-indicator"]
