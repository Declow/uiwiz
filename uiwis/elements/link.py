from uiwis.element import Element

class Link(Element):
    def __init__(self, text, link: str) -> None:
        super().__init__("a")
        self.content = text
        self.attributes["href"] = link
        self.classes("link link-hover")
