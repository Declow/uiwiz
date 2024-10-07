from typing import Callable, Optional, Union
from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class OnEvent(Element):
    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "OnEvent":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
