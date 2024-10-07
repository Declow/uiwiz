from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import ON_EVENTS


class Range(OnEvent):
    root_class: str = "range "

    def __init__(self, min: int, max: int, value: int, name: str, step: int = None) -> None:
        super().__init__("input")
        self.attributes["type"] = "range"
        self.attributes["name"] = name
        self.attributes["min"] = min
        self.attributes["max"] = max
        self.attributes["value"] = value
        if step:
            self.attributes["step"] = step

        self.classes()

    @property
    def min(self) -> int:
        return self.attributes["min"]

    @min.setter
    def min(self, value: int):
        self.attributes["min"] = value
        return self

    @property
    def max(self) -> int:
        return self.attributes["max"]

    @max.setter
    def max(self, value: int):
        self.attributes["max"] = value
        return self
