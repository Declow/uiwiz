from typing import Callable, Optional, Union
from uiwiz.element import Element


class Button(Element):
    root_class: str = "btn "

    def __init__(self, title: str) -> None:
        super().__init__(tag="button")
        self.content = title
        self.classes()
        self.inline = True

    def on_click(
        self,
        func: Optional[Callable] = None,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
    ) -> "Button":
        self.event = {
            "func": func,
            "trigger": "click",
            "target": target,
            "swap": swap,
        }
        return self
