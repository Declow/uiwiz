from uiwiz.element import Element


class Divider(Element):
    root_class = "divider "
    _classes_hor = "divider-horizontal"

    def __init__(self, text: str = "") -> None:
        super().__init__("div")
        self.content = text
        self.classes()

    def horizontal(self) -> "Divider":
        self.classes(Divider._classes_hor)
        return self
