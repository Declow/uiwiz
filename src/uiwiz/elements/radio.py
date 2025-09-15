from uiwiz.elements.extensions.on_event import OnEvent


class Radio(OnEvent):
    root_class: str = "radio"
    root_size: str = "radio-{size}"

    def __init__(self, name: str, checked: bool = False) -> None:
        """Radio

        This element is used for radio buttons

        .. code-block:: python
            from uiwiz import ui

            with ui.form():
                ui.radio("group1", checked=True)
                ui.radio("group1")

        :param name: name of the radio group
        :param checked: if the radio is checked
        """
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "radio"
        if checked:
            self.attributes["checked"] = "checked"
