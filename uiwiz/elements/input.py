from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class Input(OnEvent):
    root_class: str = "input "
    root_size: str = "input-{size}"
    _classes: str = "input-bordered w-full"

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        placeholder: Optional[str] = None,
    ) -> None:
        """Input

        This element is used for input data

        :param name: Used in the attributes name sent back in json
        :param value: The default value for the input
        :param placeholder: Text to show before input
        """
        super().__init__("input")
        self.classes(Input._classes)
        self.attributes["name"] = name
        if placeholder:
            self.placeholder = placeholder
        if value:
            self.value = value
        self.attributes["autocomplete"] = "off"

    @property
    def placeholder(self) -> Optional[str]:
        return self.attributes["placeholder"]

    @placeholder.setter
    def placeholder(self, value: str):
        self.attributes["placeholder"] = value
        return self
