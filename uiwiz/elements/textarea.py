from typing import Callable
from uiwiz.element import Element

class TextArea(Element):
    _classes: str = "textarea textarea-bordered"

    def __init__(self, placeholder: str = None, name="input", on_change: Callable = None, target: Callable = None) -> None:
        super().__init__("textarea")
        self.events.append({
            "func": on_change,
            "inputs": None,
            "trigger": "input",
            "endpoint": None,
            "target": target,
            "swap": "swap"
        })
        self.attributes["name"] = name
        self.attributes["placeholder"] = placeholder
        self.classes(TextArea._classes)