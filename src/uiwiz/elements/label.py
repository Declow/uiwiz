from typing import Optional

from uiwiz.element import Element
from uiwiz.elements.extensions.bindable import Bindable


class Label(Bindable):
    root_class: str = "label "
    root_size: str = "label-{size}"

    def __init__(self, text: Optional[str] = None, for_: Optional[Element] = None) -> None:
        """Label

        This element is used for labels that can be bound to form elements.

        .. code-block:: python
            from uiwiz import ui

            with ui.element().classes("flex flex-row gap-4"):
                label = ui.label("Username")
                input = ui.input("username")
                label.set_for(input)

            with ui.col():
                ui.label().combined_label("Password", ui.input("Password"))
                ui.label().combined_label("Type", ui.dropdown("dropdown", ["Option 1", "Option 2", "Option 3"], "Select an option"))
                ui.label().combined_label_end("Age", ui.input("Age"))
                

        :param text: The text to display
        :type text: str, optional
        :param for_: The element to bind the label to
        :type for_: Element, optional
        """
        super().__init__(tag="label")
        if text:
            self.content = text
        if for_:
            self._for = for_
            self.attributes["for"] = for_.id

        # Allign the label next to the element
        self.attributes["style"] = "padding-top: unset;"

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self

    def set_for(self, for_: Element) -> "Label":
        self._for = for_
        self.attributes["for"] = for_.id
        return self
    
    def _combined_label(self, text: str, for_: Element, label_first: bool = True) -> "Label":
        """Helper to create a label with text and bind it to an element, order controlled by label_first."""
        if text:
            self.content = text
        # Remove from previous parents
        if self.parent_element and self in self.parent_element.children:
            self.parent_element.children.remove(self)
        if for_.parent_element and for_ in for_.parent_element.children:
            for_.parent_element.children.remove(for_)
        # Create container and add children in specified order
        with Element("label").classes(for_.tag) as container:
            if label_first:
                container.children.append(self)
                container.children.append(for_)
            else:
                container.children.append(for_)
                container.children.append(self)
            self.attributes["class"] = "label"
            for_.attributes["class"] = ""
        return self

    def combined_label(self, text: str, for_: Element) -> "Label":
        """Create a label with text and bind it to an element (label first)."""
        return self._combined_label(text, for_, label_first=True)

    def combined_label_end(self, text: str, for_: Element) -> "Label":
        """Create a label with text and bind it to an element (element first)."""
        return self._combined_label(text, for_, label_first=False)