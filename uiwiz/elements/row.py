from uiwiz.element import Element

class Row(Element):
    _classes: str = "row"

    def __init__(self) -> None:
        super().__init__()

        self.classes(Row._classes)