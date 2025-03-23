from typing import Optional

from uiwiz.elements.extensions.on_event import OnEvent


class Number(OnEvent):
    root_class: str = "input "

    def __init__(self, name: str, value: int, min: int, max: int, step: Optional[int] = None) -> None:
        """Range

        This element is used for range inputs

        .. code-block:: python
            from uiwiz import ui

            ui.number("range", 50, 0, 100, 1):

        :param name: name of the range input
        :param value: default value of the range input
        :param min: minimum value of the range input
        :param max: maximum value of the range input
        :param step: step value of the range input
        """
        super().__init__("input")
        self.attributes["type"] = "number"
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
