from datetime import datetime
from typing import Optional
from uiwiz.element import Element


class Datepicker(Element):
    def __init__(self, default_date: Optional[datetime] = None) -> None:
        super().__init__("input")
        self.attributes["type"] = "date"
        if default_date:
            self.attributes["value"] = default_date.strftime("%Y-%m-%d")
