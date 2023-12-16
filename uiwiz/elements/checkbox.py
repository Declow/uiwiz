from uiwiz.element import Element


class Checkbox(Element):
    root_class: str = "checkbox "

    def __init__(self, name: str, checked: bool = False) -> None:
        _type = "input"
        if checked:
            _type += " checked"
        super().__init__(_type)
        self.attributes["name"] = name
        self.attributes["type"] = "checkbox"
        self.classes()
