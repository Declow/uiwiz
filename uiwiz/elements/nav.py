from uiwiz.element import Element


class Nav(Element):
    _classes: str = "navbar bg-base-100 bg-error"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Nav._classes)