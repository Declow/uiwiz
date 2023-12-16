from uiwiz.element import Element


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

    @property
    def min(self) -> int:
        return self.attributes["min"]

    @property
    def max(self) -> int:
        return self.attributes["max"]

    @property
    def value(self) -> int:
        return self.attributes["value"]
