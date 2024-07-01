from uiwiz.element import Element


class Toggle(Element):
    root_class: str = "toggle "

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["type"] = "checkbox"
        self.attributes["name"] = name
        self.classes()
