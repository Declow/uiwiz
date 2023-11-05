from uiwiz.element import Element

class Divider(Element):
    _classes = "divider"
    _classes_hor = "divider divider-horizontal"

    def __init__(self) -> None:
        super().__init__("div")
        self.classes(Divider._classes)
    
    def horizontal(self) -> "Divider":
        self.classes(Divider._classes_hor)
        return self