from typing import Callable
from uiwiz.element import Element


class Button(Element):
    _classes: str = "btn btn-neutral place-content-center"

    def __init__(self, title: str) -> None:
        super().__init__(tag="button")
        self.content = title
        self.classes(Button._classes)

    def on_click(self, func: Callable, inputs = None, endpoint=None, target: str = None, swap: str = None) -> "Button":
        self.event = {
            "func": func,
            "inputs": inputs,
            "trigger": "click",
            "endpoint": endpoint,
            "target": target,
            "swap": swap
        }
        return self
