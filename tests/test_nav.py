from uiwiz import ui
from uiwiz.frame import Frame


def test_nav_renders_with_default_classes() -> None:
    with ui.nav():
        ui.link("Home", "/")

    output = Frame.get_stack().render()
    assert "navbar" in output
    assert "w-full" in output
