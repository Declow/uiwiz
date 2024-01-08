from typing import Callable, Union
from uiwiz.element import Element


class Button(Element):
    root_class: str = "btn "

    def __init__(self, title: str) -> None:
        super().__init__(tag="button")
        self.content = title
        self.classes()
        self.inline = True

    def on_click(
        self, func: Callable = None, endpoint=None, target: Union[Callable, str, Element] = None, swap: str = None
    ) -> "Button":
        _target = ""
        if isinstance(target, str):
            _target = "#" + target
        if isinstance(target, Element):
            _target = "#" + target.id
        if isinstance(target, Callable):
            _target = target
        self.event = {
            "func": func,
            "trigger": "click",
            "endpoint": endpoint,
            "target": _target,
            "swap": swap,
        }
        return self
