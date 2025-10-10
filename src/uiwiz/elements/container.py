from uiwiz.element import Element


class Container(Element):
    root_class: str = "container flex flex-col mx-auto {max_w} {padding} {space_y} grow"

    def __init__(self, max_w: str = "max-w-[960px]", padding: str = "pt-4 pb-4", space_y: str = "space-y-4") -> None:
        """Container

        A container element that centers a box in the middle of the screen.
        """
        super().__init__()
        self.__root_class__ = Container.root_class.format(max_w=max_w, padding=padding, space_y=space_y)
        self.classes()
