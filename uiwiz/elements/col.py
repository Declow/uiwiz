from uiwiz.element import Element


class Col(Element):
    def __init__(self) -> None:
        super().__init__()
        self.classes("flex flex-col items-start gap-4")
