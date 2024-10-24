from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class Input(OnEvent):
    root_class: str = "input "
    _classes: str = "input-bordered w-full"

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        placeholder: Optional[str] = None,
        on_change: FUNC_TYPE = None,
        target: TARGET_TYPE = None,
        trigger: ON_EVENTS = "input",
        swap: SWAP_EVENTS = "swap",  # TODO: Fix
    ) -> None:
        """Input

        This element is used for input data

        :param placeholder: Text to show before input
        :param name: Used in the attributes name sent back in json
        :param on_change: function or method to call on change
        :param target: Function or id of the element to replace
        :param trigger: keyup, keydown, load and more see htmx docs
        """
        super().__init__("input")
        self.classes(Input._classes)
        self.attributes["name"] = name
        if placeholder:
            self.attributes["placeholder"] = placeholder
        if value:
            self.value = value
        self.attributes["autocomplete"] = "off"

        if on_change:
            self.event = {
                "func": on_change,
                "trigger": trigger,
                "target": target,
                "swap": swap,
            }

    def on(
        self,
        func: FUNC_TYPE,
        trigger: ON_EVENTS = "input",
        target: TARGET_TYPE = None,
        swap: SWAP_EVENTS = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Input":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
