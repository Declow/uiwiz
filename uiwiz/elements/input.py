from typing import Callable
from uiwiz.element import Element

class Input(Element):
    _classes: str = "input input-bordered w-full max-w-xs"

    def __init__(self, placeholder: str = None, name="input", on_change: Callable = None, target: Callable = None, trigger = "input") -> None:
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
        self.attributes["placeholder"] = placeholder
        self.auto_complete = False
        if on_change is not None:
            self.events.append({
                "func": on_change,
                "inputs": None,
                "trigger": trigger,
                "endpoint": None,
                "target": target,
                "swap": "swap"
            })
            
        