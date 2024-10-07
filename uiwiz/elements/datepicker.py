from datetime import date, datetime
from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.event import ON_EVENTS


class Datepicker(Element):
    def __init__(self, name: str, value: Optional[datetime] = None) -> None:
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "date"
        if value:
            self.default_date(value)

    def default_date(self, date: Union[datetime, date]) -> "Datepicker":
        if date is None:
            raise ValueError("Date cannot be None")
        self.value = date.strftime("%Y-%m-%d")
        return self

    def on(
        self,
        func: Callable,
        trigger: ON_EVENTS = "input",
        target: Union[Callable, str, Element] = None,
        swap: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> "Datepicker":  # type: ignore
        self.event = {"func": func, "trigger": trigger, "target": target, "swap": swap, "params": params}
        return self
