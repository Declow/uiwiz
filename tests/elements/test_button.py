from uiwiz import ui


def test_button():
    output = str(ui.button("Click me"))
    assert f'<button id="a-0" class="btn btn-md">Click me</button>' == output


def test_button_submit():
    btn = ui.button("Click me")

    @btn.stack.app.ui("/submit")
    def func():
        pass  # pragma: no cover

    btn.on_click(func)
    output = str(btn)
    print(output)
    assert (
        f'<button id="a-0" class="btn btn-md" hx-target="this" hx-swap="outerHTML" hx-post="/submit" hx-trigger="click" hx-ext="json-enc">Click me</button>'
        == output
    )
