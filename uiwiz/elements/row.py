from uiwiz.element import Element


class Row(Element):
    root_class: str = "flex flex-row {wrap} {item_position} {gap} {padding} "

    def __init__(
        self,
        wrap: str = "flex-wrap",
        item_position: str = "items-start",
        gap: str = "gap-4",
        padding: str = "",
    ) -> None:
        super().__init__()
        self.__root_class__ = Row.root_class.format(
            wrap=wrap, item_position=item_position, gap=gap, padding=padding
        )
