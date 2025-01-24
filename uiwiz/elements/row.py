from uiwiz.element import Element


class Row(Element):
    root_class: str = "flex flex-row flex-wrap items-start gap-4 "

    def __init__(self) -> None:
        super().__init__()
