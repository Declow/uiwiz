from uiwis.element import Element

class Label(Element):
    def __init__(self, text: str = "", for_: Element = None) -> None:
        super().__init__(tag="label")
        self.content = text
        if for_:
            self.attributes["for"] = for_.id

    def set_text(self, text: str) -> "Label":
        self.content = text
        return self