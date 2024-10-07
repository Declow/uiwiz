from typing import Callable, Optional, Union

from uiwiz.element import Element
from uiwiz.elements.extensions.on_event import OnEvent


class Upload(OnEvent):
    root_class: str = "file-input "
    _classes: str = "file-input-bordered file-input-sm"

    def __init__(
        self,
        name: str,
    ) -> "Upload":
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = name
        self.classes(Upload._classes)

    def on_upload(
        self,
        on_upload: Callable,
        target: Union[Callable, str, Element] = None,
        trigger: str = "change",
        swap: Optional[str] = None,
    ) -> "Upload":
        self.event = {
            "func": on_upload,
            "trigger": trigger,
            "target": target,
            "swap": swap,
            "hx-encoding": "multipart/form-data",
        }

        return self
