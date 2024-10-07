from typing import Callable, Optional, Union
from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class Radio(Element):
    root_class: str = "radio"

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "radio"
        if checked:
            self.attributes["checked"] = "checked"
        self.classes()

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Radio":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
