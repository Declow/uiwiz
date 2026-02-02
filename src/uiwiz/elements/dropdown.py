from __future__ import annotations

from collections import namedtuple

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent

DropdownItem = namedtuple("DropdownItem", ["name", "value"])


class Dropdown(OnEvent):
    root_class: str = "select "
    root_size: str = "select-{size}"
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(
        self,
        name: str,
        items: list[str] | list[DropdownItem],
        placeholder: str | None = None,
    ) -> None:
        """Dropdown

        A dropdown is a list in which the selected item is always visible, and the others are visible on demand.

        .. code-block:: python
            from uiwiz import ui

            ui.dropdown("dropdown", ["Option 1", "Option 2", "Option 3"], "Select an option")
            ui.dropdown("dropdown", ["Option 1", "Option 2", "Option 3"], "Option 1") # Option 1 is selected by default
            ui.dropdown("dropdown", [ui.dropdownItem(name="Option 1", value="1"), ui.dropdownItem(name="Option 2", value="2")], "Select an option")

        :param name: The name of the dropdown
        :type name: str
        :param items: List of items in the dropdown
        :type items: Union[list[str], list[DropdownItem]]
        :param placeholder: Placeholder text
        :type placeholder: str, optional
        """
        super().__init__("select")
        self.attributes["name"] = name
        self.classes()
        self.size(self._size)
        with self:
            if placeholder and placeholder not in items:
                Element("option disabled selected", content=placeholder)
            for v in items:
                if isinstance(v, DropdownItem):
                    e = Element("option", content=v.name)
                    e.value = v.value
                    if placeholder == v.value:
                        e.attributes["selected"] = "selected"
                else:
                    e = Element("option", content=v)
                    e.value = v
                    if placeholder == v:
                        e.attributes["selected"] = "selected"
