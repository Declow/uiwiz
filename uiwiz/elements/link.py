from uiwiz.element import Element

class Link(Element):
    _classes: str = "link link-hover"

    def __init__(self, text, link: str) -> None:
        super().__init__("a")
        self.content = text
        self.attributes["href"] = link
        self.classes(Link._classes)
