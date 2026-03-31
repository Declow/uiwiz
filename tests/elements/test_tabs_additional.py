from uiwiz import ui
from uiwiz.frame import Frame


def test_tabs_first_tab_is_activated_by_default() -> None:
    with ui.tabs():
        with ui.tab("One"):
            ui.label("one")
        with ui.tab("Two"):
            ui.label("two")

    output = Frame.get_stack().render()
    assert output.count('checked=""') == 1
