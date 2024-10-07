from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import ON_EVENTS


class Toggle(OnEvent):
    root_class: str = "toggle "

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["type"] = "checkbox"
        self.attributes["name"] = name
        self.classes()
