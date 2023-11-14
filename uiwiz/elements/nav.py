from uiwiz.element import Element


class Nav(Element):
    _classes: str = "navbar bg-[#6499E9]"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Nav._classes)