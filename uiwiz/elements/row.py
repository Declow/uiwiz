from uiwiz.element import Element


class Row(Element):
    root_class: str = "row "

    def __init__(self) -> None:
        super().__init__()

        self.classes()
