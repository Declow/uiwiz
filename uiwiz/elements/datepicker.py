from datetime import date, datetime
from typing import Optional, Union

from uiwiz.element import Element


class Datepicker(Element):
    def __init__(self, name: str, default_date: Optional[datetime] = None) -> None:
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["type"] = "date"
        if default_date:
            self.default_date(default_date)

    def default_date(self, date: Union[datetime, date]):
        if date is None:
            raise Exception("Date cannot be None")
        self.value = date.strftime("%Y-%m-%d")
