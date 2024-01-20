from typing import Callable, Optional, Union
from uiwiz.element import Element


class Form(Element):
    root_class: str = "col "

    def __init__(self) -> None:
        super().__init__("form")
        self.classes()

    def on_submit(
        self,
        func: Optional[Callable] = None,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = "beforeend",
    ):
        self.event = {
            "func": func,
            "trigger": "submit",
            "target": target,
            "swap": swap,
        }
        return self
