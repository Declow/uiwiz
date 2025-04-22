from typing import Any, Optional

from uiwiz.element import Element


class HiddenInput(Element):
    _classes: str = ""

    def __init__(
        self,
        name: str,
        value: Optional[Any] = None,
    ) -> None:
        """HiddenInput

        This element is used for hidden input data

        :param name: Used in the attributes name sent back in json
        :type name: str
        :param value: The value to send back
        :type value: Any
        """
        super().__init__("input")
        self.attributes["name"] = name
        self.attributes["value"] = value
        self.attributes["type"] = "hidden"
