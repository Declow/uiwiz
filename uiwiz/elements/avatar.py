from uiwiz.element import Element

class Avatar(Element):
    _classes: str = "avatar"
    _classes_inner: str = "w-{size} rounded-full"
    
    def __init__(self, path: str, size: int = 12) -> None:
        super().__init__()
        self.classes(Avatar._classes)
        with self:
            with Element("div").classes(Avatar._classes_inner.format(size=size)):
                img = Element("img")
                img.attributes["src"] = path
