from uiwiz import ui
from uiwiz.frame import Frame


def test_drawer_side_context_preserves_parent_stack() -> None:
    with ui.drawer() as drawer:
        with drawer.drawer_content():
            ui.label("content")
        with drawer.drawer_side():
            with ui.element("li"):
                ui.link("item", "/")
        ui.label("after")

    output = Frame.get_stack().render()
    assert "after" in output
    assert output.count("drawer-content") == 1
    assert output.count("drawer-side") == 1
