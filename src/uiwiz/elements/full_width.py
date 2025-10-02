from uiwiz.element import Element


class FullWidth(Element):
    root_class = "w-full"

    def __init__(self) -> None:
        """FullWidth

        This element is used to create a full-width container.

        .. code-block:: python
            from uiwiz import ui

            with ui.full_width():
                ui.text("This is a full-width container")

        """
        super().__init__()
        self.classes(FullWidth.root_class)
