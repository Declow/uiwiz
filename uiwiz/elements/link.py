from uiwiz.element import Element


class Link(Element):
    root_class: str = "link "
    _classes: str = "link-hover"

    def __init__(self, text: str, link: str) -> None:
        super().__init__("a")
        self.content = text
        self.attributes["href"] = link
        self.classes(Link._classes)
