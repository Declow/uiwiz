from unittest import mock

from uiwiz import ui
from uiwiz.app import UiwizApp
from uiwiz.frame import Frame
from uiwiz.page_route import PageRouter


def test_button():
    output = str(ui.button("Click me"))
    assert f'<button id="a-0" type="button" class="btn ">Click me</button>' == output


def test_button_submit():
    btn = ui.button("Click me")

    @btn.stack.app.ui("/submit")
    def func():
        pass

    btn.on_click(func)
    output = str(btn)
    print(output)
    assert (
        f'<button id="a-0" type="button" class="btn " hx-target="this" hx-swap="outerHTML" hx-post="/submit" hx-trigger="click" hx-ext="json-enc">Click me</button>'
        == output
    )
