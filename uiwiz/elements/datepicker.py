from datetime import date, datetime
from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import ON_EVENTS


class Datepicker(OnEvent):
    def __init__(
        self,
        name: str,
        value: Optional[datetime] = None,
    ) -> None:
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
