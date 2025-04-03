from typing import Optional

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent


class Dropdown(OnEvent):
    root_class: str = "select "
    root_size: str = "select-{size}"
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(self, name: str, items: list[str], placeholder: Optional[str] = None) -> None:
        """Dropdown

        A dropdown is a list in which the selected item is always visible, and the others are visible on demand.

        .. code-block:: python
            from uiwiz import ui

            ui.dropdown("dropdown", ["Option 1", "Option 2", "Option 3"], "Select an option")
            ui.dropdown("dropdown", ["Option 1", "Option 2", "Option 3"], "Option 1") # Option 1 is selected by default

        :param name: The name of the dropdown
        :type name: str
        :param items: List of items in the dropdown
        :type items: list[str]
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
                e = Element("option", content=v)
                e.value = v
                if placeholder == v:
                    e.attributes["selected"] = "selected"
