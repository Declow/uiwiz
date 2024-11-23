from typing import Optional

from uiwiz.elements.extensions.on_event import OnEvent


class Range(OnEvent):
    root_class: str = "range "
    root_size: str = "range-{size}"

    def __init__(self, name: str, value: int, min: int, max: int, step: Optional[int] = None) -> None:
        super().__init__("input")
        self.attributes["type"] = "range"
        self.attributes["name"] = name
        self.attributes["min"] = min
        self.attributes["max"] = max
        self.attributes["value"] = value
        if step:
            self.attributes["step"] = step

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
