from uiwiz.elements.extensions.on_event import OnEvent


class Toggle(OnEvent):
    root_class: str = "toggle"
    root_size: str = "toggle-{size}"

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["type"] = "checkbox"
        self.attributes["name"] = name
