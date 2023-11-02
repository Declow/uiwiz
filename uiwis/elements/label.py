from uiwis.element import Element

class Label(Element):
    def __init__(self, text: str = "") -> None:
        super().__init__(tag="div")
        self.content = text

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self