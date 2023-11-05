from uiwiz.element import Element

class Radio(Element):
    _classes: str = "radio"

    def __init__(self, name, value) -> None:
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "radio"
        self.attributes["value"] = value
        self.classes(Radio._classes)