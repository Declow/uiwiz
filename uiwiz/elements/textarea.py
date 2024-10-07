from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import ON_EVENTS


class TextArea(OnEvent):
    root_class: str = "textarea "
    _classes: str = "textarea-bordered w-full"

    def __init__(
        self,
        placeholder: str = None,
        name: str = "input",
        value: str = None,
        on_change: Callable = None,
        target: Callable = None,
        trigger: Optional[ON_EVENTS] = "input",
        swap: str = "swap",
    ) -> None:
        super().__init__("textarea")
        self.attributes["name"] = name
        if placeholder:
            self.attributes["placeholder"] = placeholder
        if value:
            self.content = value
        self.classes(TextArea._classes)

        if on_change:
            self.event = {
                "func": on_change,
                "trigger": trigger,
                "target": target,
                "swap": swap,
            }

    @property
    def placeholder(self) -> Optional[str]:
        return self.attributes["placeholder"]

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS = "input",
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "TextArea":  # type: ignore
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
