from uiwiz.element import Element


class Container(Element):
    root_class: str = "container flex flex-col mx-auto max-w-[960px] pt-4 pb-4 space-y-4 grow"

    def __init__(self) -> None:
        """Container

        A container element that centers its children.
        """
        super().__init__()
        self.classes()
