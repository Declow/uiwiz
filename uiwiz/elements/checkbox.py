from typing import Callable, Optional, Union
from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class Checkbox(Element):
    root_class: str = "checkbox "

    def __init__(self, name: str, checked: bool = False) -> None:
        super().__init__("input")
        if checked:
            self.attributes["checked"] = "checked"
        self.attributes["name"] = name
        self.attributes["type"] = "checkbox"
        self.classes()

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Checkbox":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
