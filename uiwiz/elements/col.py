from uiwiz.element import Element


class Col(Element):
    root_class: str = "flex flex-col {item_position} {gap} {padding} "

    def __init__(
        self,
        item_position: str = "items-start",
        gap: str = "gap-4",
        padding: str = "p-4",
    ) -> None:
        """Col

        Align children elements horizontally.

        :param item_position: The position of the items in the column. Items-start by default and will align the items to the left. items-end will align the items to the right.
        :type item_position: str, optional
        :param gap: The gap between the items in the column.
        :type gap: str, optional
        :param padding: The padding of the column.
        :type padding: str, optional
        """
        super().__init__()
        self.__root_class__ = Col.root_class.format(item_position=item_position, gap=gap, padding=padding)
        self.classes("")
