from typing import Callable
from uiwis.element import Element

class Form(Element):
    def __init__(self) -> None:
        super().__init__("form")
        self.classes("col")
    
    def on_submit(self, func: Callable, endpoint: str = None):
        self.events.append({
            "func": func,
            "endpoint": endpoint,
            "_type": "submit",
            "target": "this",
            "swap": "beforeend",
        })
        return self