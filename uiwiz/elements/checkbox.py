from uiwiz.element import Element


class Checkbox(Element):
    root_class: str = "checkbox "

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["name"] = name
        self.attributes["type"] = "checkbox"
        self.classes()
