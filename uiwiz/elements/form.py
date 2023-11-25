from typing import Callable
from uiwiz.element import Element

class Form(Element):
    _classes: str = "col"

    def __init__(self) -> None:
        super().__init__("form")
        self.classes(Form._classes)
    
    def on_submit(self, func: Callable, endpoint: str = None):
        self.event = {
            "func": func,
            "endpoint": endpoint,
            "trigger": "submit",
            "target": "this",
            "swap": "beforeend",
        }
        return self