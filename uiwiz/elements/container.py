from uiwiz.element import Element


class Container(Element):
    root_class: str = "container flex flex-col mx-auto max-w-[960px] pt-2 pb-2"

    def __init__(self) -> None:
        """Container

        A container element that centers its children.
        """
        super().__init__()
        self.classes()
