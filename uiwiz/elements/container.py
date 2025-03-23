from uiwiz.elements.col import Col


class Container(Col):
    root_class: str = "container mx-auto max-w-[960px]"

    def __init__(self) -> None:
        """Container

        A container element that centers its children.
        """
        super().__init__()
        self.classes(super().root_class)
