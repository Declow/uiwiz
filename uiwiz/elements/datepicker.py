from datetime import date, datetime
from typing import Optional, Union

from uiwiz.elements.extensions.on_event import OnEvent


class Datepicker(OnEvent):
    def __init__(
        self,
        name: str,
        value: Optional[datetime] = None,
    ) -> None:
        """Datepicker element

        :param name: name of the datepicker
        :type name: str
        :param value: default value of the datepicker
        :type value: datetime, optional
        """
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
