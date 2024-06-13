from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.checkbox import Checkbox
from uiwiz.elements.input import Input
from uiwiz.elements.textarea import TextArea

# from uiwiz.elements.


@dataclass
class UiAnno:
    type: Union[Input, TextArea, Checkbox] = None
    placeholder: Optional[str] = None
    classes: Optional[str] = None


class Form(Element):
    root_class: str = ""

    def __init__(self) -> None:
        super().__init__("form")
        self.classes()

    def on_submit(
        self,
        func: Optional[Callable] = None,
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = "none",
        params: Optional[dict[str, str]] = None,
    ):
        self.event = {"func": func, "trigger": "submit", "target": target, "swap": swap, "params": params}
        return self
