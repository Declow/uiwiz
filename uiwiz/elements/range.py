from typing import Callable, Optional, Union
from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class Range(Element):
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

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Range":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self

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
