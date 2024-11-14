from uiwiz.element import Element


class Nav(Element):
    root_class: str = "navbar w-full "
    root_size: str = "navbar-{size}"

    def __init__(self) -> None:
        super().__init__()
