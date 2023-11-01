from uiwis.element import Element


class Nav(Element):
    def __init__(self) -> None:
        super().__init__()
        self._classes = "navbar bg-base-100 bg-error"