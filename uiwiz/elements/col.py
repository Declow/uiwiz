from uiwiz.element import Element


class Col(Element):
    root_class: str = "flex flex-col items-start gap-4 p-4 "

    def __init__(self) -> None:
        super().__init__()
