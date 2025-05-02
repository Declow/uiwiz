from typing import Optional

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent


class Input(OnEvent):
    root_class: str = "input "
    root_size: str = "input-{size}"
    _classes: str = "input-bordered w-full"

    def __init__(
        self, name: Optional[str] = None, value: Optional[str] = None, placeholder: Optional[str] = None
    ) -> None:
        """Input

        This element is used for input data

        :param name: Used in the attributes name sent back in json
        :type name: str, optional
        :param value: The default value for the input
        :type value: str, optional
        :param placeholder: Text to show before input
        :type placeholder: str, optional
        """
        super().__init__("input")
        self.classes(Input._classes)
        self.attributes["name"] = name
        self.placeholder = placeholder
        if value:
            self.value = value
        self.attributes["autocomplete"] = "off"

    @property
    def placeholder(self) -> Optional[str]:
        return self.attributes.get("placeholder")

    @placeholder.setter
    def placeholder(self, value: Optional[str]):
        if value:
            self.attributes["placeholder"] = value
        return self

    def set_placeholder(self, value: str) -> "Input":
        self.placeholder = value
        return self

    def set_floating_label(self, label: Optional[str] = None) -> "Input":
        if self.placeholder is None:
            raise ValueError("Placeholder must be set before floating label")

        self.parent_element.children.remove(self)
        with Element("label").classes("floating-label") as container:
            value = label if label else self.placeholder
            self.label_text = Element("span", content=value)
            container.children.append(self)
            self.parent_element = container

        return self
