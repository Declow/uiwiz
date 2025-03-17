from uiwiz.element import Element


class Col(Element):
    root_class: str = "flex flex-col {item_position} {gap} {padding} "

    def __init__(
        self,
        item_position: str = "items-start",
        gap: str = "gap-4",
        padding: str = "p-4",
    ) -> None:
        super().__init__()
        # format
        self.__root_class__ = Col.root_class.format(
            item_position=item_position, gap=gap, padding=padding
        )
