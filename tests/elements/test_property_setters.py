from uiwiz import ui


def test_input_set_placeholder_returns_self() -> None:
    element = ui.input("name")
    assert element.set_placeholder("Name") is element


def test_textarea_placeholder_assignment_sets_attribute() -> None:
    element = ui.textarea("notes")
    element.placeholder = "Notes"
    assert element.attributes.get("placeholder") == "Notes"


def test_number_min_max_assignment_sets_attributes() -> None:
    element = ui.number("qty", 1, 0, 10)
    element.min = 2
    element.max = 20
    assert element.attributes.get("min") == 2
    assert element.attributes.get("max") == 20


def test_range_min_max_assignment_sets_attributes() -> None:
    element = ui.range("progress", 10, 0, 100)
    element.min = 5
    element.max = 95
    assert element.attributes.get("min") == 5
    assert element.attributes.get("max") == 95
