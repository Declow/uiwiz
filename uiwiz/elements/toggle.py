from uiwiz.elements.extensions.on_event import OnEvent


class Toggle(OnEvent):
    root_class: str = "toggle"
    root_size: str = "toggle-{size}"

    def __init__(self, name: str, checked: bool = False) -> None:
        """Toggle

        This element is used for toggle inputs

        .. code-block:: python
            from uiwiz import ui

            ui.toggle("toggle", True):

        :param name: name of the toggle input
        :param checked: default checked state of the toggle input
        """
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["type"] = "checkbox"
        self.attributes["name"] = name
