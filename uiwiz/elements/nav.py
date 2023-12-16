from uiwiz.element import Element


class Nav(Element):
    root_class: str = "navbar w-full "
    _classes: str = "bg-base-200"

    def __init__(self) -> None:
        super().__init__()
        self.classes(Nav._classes)
