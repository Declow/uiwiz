from uiwis.element import Element

class Toggle(Element):
    def __init__(self, name: str, checked: bool = False) -> None:
        _type = "input"
        if checked:
            _type += " checked"
        super().__init__(_type)
        self.attributes["type"] = "checkbox"
        self.classes("toggle")