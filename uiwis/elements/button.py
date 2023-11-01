from typing import Callable
from uiwis.element import Element, Event


class Button(Element):
    def __init__(self, title: str) -> None:
        super().__init__(tag="button")
        self.content = title
        self._classes = "btn btn-neutral place-content-center"


    def on_click(self, func: Callable, inputs = None, endpoint=None, target: str = None, swap: str = None) -> "Button":
        self.events.append({
            "func": func,
            "inputs": inputs,
            "_type": "click",
            "endpoint": endpoint,
            "target": target,
            "swap": swap
        })
        return self
