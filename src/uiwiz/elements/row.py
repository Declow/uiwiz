from uiwiz.element import Element


class Row(Element):
    root_class: str = "flex flex-row {wrap} {item_position} {gap} {padding}"

    def __init__(
        self,
        wrap: str = "flex-wrap",
        item_position: str = "items-start",
        gap: str = "gap-4",
        padding: str = "",
    ) -> None:
        """Row

        Align children elements vertically.

        .. code-block:: python
            from uiwiz import ui

            with ui.row():
                ui.label("Hello")
                ui.label("World")

        :param wrap: The wrap of the row. Flex-wrap by default and will wrap the items to the next row if they don't fit.
        :param item_position: The position of the items in the row. Items-start by default and will align the items to the left. items-end will align the items to the right.
        :param gap: The gap between the items in the row.
        :param padding: The padding of the row.
        """
        super().__init__()
        self.__root_class__ = Row.root_class.format(wrap=wrap, item_position=item_position, gap=gap, padding=padding)
        self.classes("")
