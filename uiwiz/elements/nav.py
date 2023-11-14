from uiwiz.element import Element


class Nav(Element):
    _classes: str = "navbar bg-[#5898d4]"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Nav._classes)