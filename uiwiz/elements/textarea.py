from typing import Callable, Optional
from uiwiz.element import Element


class TextArea(Element):
    root_class: str = "textarea "
    _classes: str = "textarea-bordered"

    def __init__(
        self,
        placeholder: str = None,
        name="input",
        on_change: Callable = None,
        target: Callable = None,
        trigger: str = "input",
    ) -> None:
        super().__init__("textarea")
        self.attributes["name"] = name
        self.attributes["placeholder"] = placeholder
        self.inline = True
        self.classes(TextArea._classes)

        if on_change:
            self.event = {
                "func": on_change,
                "inputs": None,
                "trigger": trigger,
                "endpoint": None,
                "target": target,
                "swap": "swap",
            }

    @property
    def placeholder(self) -> Optional[str]:
        return self.attributes["placeholder"]
