from uiwiz.element import Element


class Row(Element):
    def __init__(self) -> None:
        super().__init__()

        self.classes("flex flex-row flex-wrap items-start gap-4")
