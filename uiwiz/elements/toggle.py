from uiwiz.element import Element

class Toggle(Element):
    _classes: str = "toggle"

    def __init__(self, name: str, checked: bool = False) -> None:
        _type = "input"
        if checked:
            _type += " checked"
        super().__init__(_type)
        self.attributes["type"] = "checkbox"
        self.attributes["name"] = name
        self.classes(Toggle._classes)