from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.event import FUNC_TYPE, SWAP_EVENTS, TARGET_TYPE


class Form(Element):
    root_class: str = "flex flex-col items-start gap-4 p-4 "

    def __init__(self) -> None:
        super().__init__("form")

    def on_submit(
        self,
        func: FUNC_TYPE = None,
        target: TARGET_TYPE = None,
        swap: SWAP_EVENTS = "none",
        params: Optional[dict[str, str]] = None,
    ):
        self.event = {"func": func, "trigger": "submit", "target": target, "swap": swap, "params": params}
        return self
