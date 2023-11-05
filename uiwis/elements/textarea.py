from typing import Callable
from uiwis.element import Element

class TextArea(Element):
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
        self.classes("textarea textarea-bordered")