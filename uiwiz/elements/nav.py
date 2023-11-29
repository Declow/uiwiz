from uiwiz.element import Element


class Nav(Element):
    _classes: str = "w-full navbar"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Nav._classes)