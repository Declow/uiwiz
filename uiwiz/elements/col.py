from uiwiz.element import Element

class Col(Element):
    _classes = "col"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Col._classes)

