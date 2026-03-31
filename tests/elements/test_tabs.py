from uiwiz import ui
from uiwiz.frame import Frame


def test_tabs_with_no_children_does_not_crash() -> None:
    with ui.tabs():
        pass

    output = Frame.get_stack().render()
    assert 'role="tablist"' in output
