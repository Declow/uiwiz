from uiwiz.element import Element


class Col(Element):
    root_class = "col "

    def __init__(self) -> None:
        super().__init__()
        self.classes()
