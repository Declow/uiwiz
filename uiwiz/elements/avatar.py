from uiwiz.element import Element

class Avatar(Element):
    def __init__(self, path: str) -> None:
        super().__init__("div")
        self.classes("avatar")
        with self:
            with Element("div").classes("w-16 rounded-full"):
                img = Element("img")
                img.attributes["src"] = path
