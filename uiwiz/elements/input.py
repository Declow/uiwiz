from typing import Callable, Optional, Union

from uiwiz.element import Element


class Input(Element):
    root_class: str = "input "
    _classes: str = "input-bordered w-full"

    def __init__(
        self,
        placeholder: str = None,
        name=None,
        on_change: Optional[Callable] = None,
        target: Optional[Callable] = None,
        trigger: str = "input",
        swap: Optional[str] = "swap",
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
        func: Callable,
        target: Union[Callable, str, Element] = None,
        trigger: str = "input",
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Input":
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
