from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class TextArea(OnEvent):
    root_class: str = "textarea "
    _classes: str = "textarea-bordered w-full"

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        placeholder: Optional[str] = None,
        on_change: FUNC_TYPE = None,
        target: TARGET_TYPE = None,
        trigger: ON_EVENTS = "input",
        swap: SWAP_EVENTS = "swap",
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
        func: FUNC_TYPE,
        trigger: ON_EVENTS = "input",
        target: TARGET_TYPE = None,
        swap: SWAP_EVENTS = None,
        params: Optional[dict[str, str]] = None,
    ) -> "TextArea":  # type: ignore
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
