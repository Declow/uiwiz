from uiwiz.element import Element


class Radio(Element):
    root_class: str = "radio"

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "radio"
        if checked:
            self.attributes["checked"] = "checked"
        self.classes()
