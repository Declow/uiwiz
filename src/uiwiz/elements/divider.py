from uiwiz.element import Element


class Divider(Element):
    root_class = "divider "
    _classes_hor = "divider-horizontal"

    def __init__(self, text: str = "") -> None:
        """Divider

        Display a divider line between elements.

        Example:
        .. code-block:: python

            from uiwiz import ui

            with ui.col():
                ui.button("Button 1")
                ui.divider("or")
                ui.button("Button 2")

        :param text: The text to display in the divider.
        :type text: str, optional
        """
        super().__init__("div")
        self.content = text

    def horizontal(self) -> "Divider":
        self.classes(Divider._classes_hor)
        return self
