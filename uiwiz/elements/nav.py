from uiwiz.element import Element


class Nav(Element):
    root_class: str = "navbar w-full "

    def __init__(self) -> None:
        super().__init__()
        self.classes()
