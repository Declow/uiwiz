from typing import Callable, Optional, Union
from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class Dropdown(Element):
    root_class: str = "select "
    _classes: str = "select-bordered w-full max-w-xs"

    def __init__(self, name: str, items: list[str], placeholder: str = None) -> None:
        super().__init__("select")
        self.attributes["name"] = name
        self.classes()
        with self:
            if placeholder and placeholder not in items:
                Element("option disabled selected", content=placeholder)
            for v in items:
                e = Element("option", content=v)
                e.value = v
                if placeholder == v:
                    e.attributes["selected"] = "selected"

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Dropdown":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
